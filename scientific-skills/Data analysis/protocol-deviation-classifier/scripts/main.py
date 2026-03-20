#!/usr/bin/env python3
"""
Protocol Deviation Classifier
Clinical trial protocol deviation classification tool

Based on GCP/ICH E6 guidelines, automatically determines whether a deviation is a "major deviation" or "minor deviation".
Technical: Risk-based quality management, GCP compliance assessment, deviation classification
"""

import argparse
import json
import sys
import re
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime


class Classification(Enum):
    """Deviation classification enum"""
    MAJOR = "major"
    MINOR = "minor"
    CRITICAL = "critical"
    
    def __str__(self):
        mapping = {
            Classification.MAJOR: "Major Deviation",
            Classification.MINOR: "Minor Deviation",
            Classification.CRITICAL: "Critical Deviation"
        }
        return mapping.get(self, self.value)
    
    @property
    def en_name(self):
        mapping = {
            Classification.MAJOR: "Major Deviation",
            Classification.MINOR: "Minor Deviation",
            Classification.CRITICAL: "Critical Deviation"
        }
        return mapping.get(self, self.value.title())


class RiskLevel(Enum):
    """Risk level enum"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
    def __str__(self):
        mapping = {
            RiskLevel.NONE: "None",
            RiskLevel.LOW: "Low",
            RiskLevel.MEDIUM: "Medium",
            RiskLevel.HIGH: "High"
        }
        return mapping.get(self, self.value)
    
    @property
    def score(self):
        """Return risk score for calculation"""
        scores = {
            RiskLevel.NONE: 0,
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3
        }
        return scores.get(self, 0)


@dataclass
class DeviationEvent:
    """Protocol deviation event data class"""
    id: str = ""
    description: str = ""
    deviation_type: str = ""
    occurrence_date: Optional[str] = None
    site_id: Optional[str] = None
    subject_id: Optional[str] = None
    safety_impact: RiskLevel = RiskLevel.NONE
    data_impact: RiskLevel = RiskLevel.NONE
    scientific_impact: RiskLevel = RiskLevel.NONE
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'DeviationEvent':
        """Create event from dictionary"""
        def parse_risk(value):
            if isinstance(value, str):
                try:
                    return RiskLevel(value.lower())
                except ValueError:
                    return RiskLevel.NONE
            return RiskLevel.NONE
        
        factors = data.get('severity_factors', {})
        return cls(
            id=data.get('id', ''),
            description=data.get('description', ''),
            deviation_type=data.get('type', data.get('deviation_type', '')),
            occurrence_date=data.get('occurrence_date'),
            site_id=data.get('site_id'),
            subject_id=data.get('subject_id'),
            safety_impact=parse_risk(factors.get('safety_impact', 'none')),
            data_impact=parse_risk(factors.get('data_impact', 'none')),
            scientific_impact=parse_risk(factors.get('scientific_impact', 'none'))
        )


@dataclass
class ClassificationResult:
    """Classification result data class"""
    id: str
    classification: Classification
    confidence: float
    rationale: str
    safety_risk: RiskLevel
    data_integrity_risk: RiskLevel
    scientific_validity_risk: RiskLevel
    risk_score: int
    regulatory_basis: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    key_indicators: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "classification": str(self.classification),
            "classification_en": self.classification.en_name,
            "confidence": round(self.confidence, 2),
            "rationale": self.rationale,
            "risk_factors": {
                "safety_risk": str(self.safety_risk),
                "data_integrity_risk": str(self.data_integrity_risk),
                "scientific_validity_risk": str(self.scientific_validity_risk)
            },
            "risk_score": self.risk_score,
            "regulatory_basis": self.regulatory_basis,
            "recommended_actions": self.recommended_actions,
            "key_indicators": self.key_indicators
        }


class DeviationClassifier:
    """
    Protocol deviation classifier
    
    Based on GCP/ICH E6 guidelines, automatically determines the severity of clinical trial deviations.
    """
    
    # Major deviation keyword patterns (Chinese and English)
    MAJOR_INDICATORS = {
        'informed_consent': [
            r'知情同意', r'未获得.*同意', r'同意书', r'informed consent',
            r'未签署', r'consent', r'signed.*consent'
        ],
        'eligibility': [
            r'入选标准', r'排除标准', r'不符合.*入组', r'eligibility',
            r'inclusion.*criteria', r'exclusion.*criteria', r'ineligible'
        ],
        'dosing': [
            r'超剂量', r'双倍剂量', r'overdose', r'过量', r'错误.*剂量',
            r'wrong dose', r'double dose', r'dosing error'
        ],
        'concomitant': [
            r'合并用药', r'禁忌.*用药', r'concomitant', r'prohibited medication',
            r'forbidden drug'
        ],
        'randomization': [
            r'随机化.*错误', r'错.*随机', r'randomization error',
            r'wrong randomization'
        ],
        'safety_reporting': [
            r'SAE', r'SUSAR', r'安全性.*报告', r'漏报', r'延迟报告',
            r'serious adverse event', r'safety reporting'
        ],
        'blinding': [
            r'破盲', r'unblind', r'破盲.*未', r'未授权.*破盲'
        ],
        'data_integrity': [
            r'伪造', r'篡改', r'数据.*虚假', r'falsified',
            r'fabricated', r'数据造假'
        ],
        'critical_procedures': [
            r'关键.*未执行', r'未.*关键', r'遗漏.*主要终点',
            r'primary endpoint.*missed', r'critical procedure'
        ]
    }
    
    # Minor deviation keyword patterns
    MINOR_INDICATORS = {
        'visit_window': [
            r'访视.*延迟', r'访视.*提前', r'visit.*window',
            r'访视.*[12].*天', r'visit.*[12].*day'
        ],
        'sample_collection': [
            r'样本.*延迟', r'采样.*时间', r'sample.*delay',
            r'非关键.*样本', r'non-critical sample'
        ],
        'questionnaire': [
            r'问卷', r'日记卡', r'questionnaire', r'diary card',
            r'QOL', r'生活质量'
        ],
        'documentation': [
            r'签名.*延迟', r'文档.*缺失', r'document.*missing',
            r'signature.*delay', r'记录.*延迟'
        ],
        'non_critical': [
            r'非关键', r'次要', r'轻微', r'non-critical',
            r'minor', r'slight'
        ]
    }
    
    # Regulatory basis
    REGULATORY_BASIS = {
        'major': [
            "ICH E6(R2) Section 4.5 - Subject Safety",
            "ICH E6(R2) Section 4.9 - Informed Consent",
            "GCP Section 6.2 - Subject Rights",
            "FDA 21 CFR Part 312.60 - General Investigator Obligations"
        ],
        'minor': [
            "ICH E6(R2) Section 4.6 - Investigational Product",
            "ICH E6(R2) Section 5.1 - Trial Management",
            "GCP Section 6.4.4 - Protocol Compliance"
        ],
        'critical': [
            "ICH E6(R2) Section 2.13 - Data Integrity",
            "ICH E6(R2) Section 4.1.5 - Fraud Prevention",
            "FDA 21 CFR Part 312.70 - Disqualification of Investigators"
        ]
    }
    
    def __init__(self):
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns"""
        self.major_patterns = {
            category: [re.compile(p, re.IGNORECASE) for p in patterns]
            for category, patterns in self.MAJOR_INDICATORS.items()
        }
        self.minor_patterns = {
            category: [re.compile(p, re.IGNORECASE) for p in patterns]
            for category, patterns in self.MINOR_INDICATORS.items()
        }
    
    def classify(
        self,
        description: str,
        deviation_type: str = "",
        event_id: str = "",
        safety_impact: Optional[RiskLevel] = None,
        data_impact: Optional[RiskLevel] = None,
        scientific_impact: Optional[RiskLevel] = None
    ) -> ClassificationResult:
        """
        Classify a single deviation event
        
        Args:
            description: Deviation description
            deviation_type: Deviation type
            event_id: Event ID
            safety_impact: Safety impact level (if known)
            data_impact: Data integrity impact level (if known)
            scientific_impact: Scientific validity impact level (if known)
        
        Returns:
            ClassificationResult: Classification result
        """
        # If impact levels are not provided, auto-determine based on description
        if safety_impact is None:
            safety_impact = self._assess_safety_impact(description, deviation_type)
        if data_impact is None:
            data_impact = self._assess_data_impact(description, deviation_type)
        if scientific_impact is None:
            scientific_impact = self._assess_scientific_impact(description, deviation_type)
        
        # Calculate risk score
        risk_score = (
            safety_impact.score * 3 +
            data_impact.score * 2 +
            scientific_impact.score * 2
        )
        
        # Apply classification rules
        classification, confidence = self._apply_classification_rules(
            safety_impact, data_impact, scientific_impact, risk_score, description
        )
        
        # Generate classification rationale
        rationale = self._generate_rationale(
            classification, safety_impact, data_impact, scientific_impact, description
        )
        
        # Get key indicators
        key_indicators = self._extract_key_indicators(description, deviation_type)
        
        # Get regulatory basis
        regulatory_basis = self._get_regulatory_basis(classification, description)
        
        # Generate recommended actions
        recommended_actions = self._get_recommended_actions(classification)
        
        return ClassificationResult(
            id=event_id or self._generate_event_id(),
            classification=classification,
            confidence=confidence,
            rationale=rationale,
            safety_risk=safety_impact,
            data_integrity_risk=data_impact,
            scientific_validity_risk=scientific_impact,
            risk_score=risk_score,
            regulatory_basis=regulatory_basis,
            recommended_actions=recommended_actions,
            key_indicators=key_indicators
        )
    
    def classify_batch(self, events: List[Dict]) -> List[ClassificationResult]:
        """
        Batch classify deviation events
        
        Args:
            events: List of deviation event dictionaries
        
        Returns:
            List[ClassificationResult]: List of classification results
        """
        results = []
        for event_data in events:
            event = DeviationEvent.from_dict(event_data)
            result = self.classify(
                description=event.description,
                deviation_type=event.deviation_type,
                event_id=event.id,
                safety_impact=event.safety_impact,
                data_impact=event.data_impact,
                scientific_impact=event.scientific_impact
            )
            results.append(result)
        return results
    
    def _assess_safety_impact(self, description: str, deviation_type: str) -> RiskLevel:
        """Assess impact on subject safety"""
        text = f"{description} {deviation_type}".lower()
        
        # High safety impact keywords
        high_risk = [
            r'overdose', r'超剂量', r'双倍剂量', r'禁忌用药', r'过敏反应',
            r'严重不良事件', r'sae', r'死亡', r'危及生命', r'住院',
            r'death', r'life-threatening', r'hospitalization'
        ]
        
        # Medium safety impact keywords
        medium_risk = [
            r'不良反应', r'副作用', r'adverse event', r'合并用药',
            r'concomitant', r'药物相互作用', r'drug interaction',
            r'剂量调整', r'dose adjustment'
        ]
        
        for pattern in high_risk:
            if re.search(pattern, text, re.IGNORECASE):
                return RiskLevel.HIGH
        
        for pattern in medium_risk:
            if re.search(pattern, text, re.IGNORECASE):
                return RiskLevel.MEDIUM
        
        # If involves informed consent but no specific harm
        if re.search(r'知情同意|consent', text, re.IGNORECASE):
            return RiskLevel.HIGH
        
        return RiskLevel.NONE
    
    def _assess_data_impact(self, description: str, deviation_type: str) -> RiskLevel:
        """Assess impact on data integrity"""
        text = f"{description} {deviation_type}".lower()
        
        # High data impact
        high_patterns = [
            r'伪造|篡改|虚假|falsif|fabricat',
            r'数据.*丢失|data.*lost',
            r'关键.*数据.*缺失|critical.*data.*missing'
        ]
        
        # Medium data impact
        medium_patterns = [
            r'主要终点|primary endpoint',
            r'关键访视|critical visit',
            r'未.*评估|not.*assess'
        ]
        
        for pattern in high_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return RiskLevel.HIGH
        
        for pattern in medium_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return RiskLevel.MEDIUM
        
        return RiskLevel.LOW
    
    def _assess_scientific_impact(self, description: str, deviation_type: str) -> RiskLevel:
        """Assess impact on trial scientific validity"""
        text = f"{description} {deviation_type}".lower()
        
        # Check if it affects primary endpoint or randomization
        high_patterns = [
            r'随机化.*错误|错.*随机|randomiz',
            r'主要终点|primary endpoint',
            r'入组.*错误|错.*入组|不符合.*入组|ineligible'
        ]
        
        # Medium impact
        medium_patterns = [
            r'访视.*缺失|missed visit',
            r'疗效.*评估|efficacy assessment',
            r'破盲|unblind'
        ]
        
        for pattern in high_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return RiskLevel.HIGH
        
        for pattern in medium_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return RiskLevel.MEDIUM
        
        return RiskLevel.NONE
    
    def _apply_classification_rules(
        self,
        safety_impact: RiskLevel,
        data_impact: RiskLevel,
        scientific_impact: RiskLevel,
        risk_score: int,
        description: str
    ) -> Tuple[Classification, float]:
        """
        Apply classification rules
        
        Classification rules:
        - Any dimension is High → Major deviation
        - Safety dimension is Medium and data/scientific is Medium+ → Major deviation
        - Involves informed consent issue → Major deviation
        - Involves data falsification → Critical deviation
        - Other cases → Minor deviation
        """
        text = description.lower()
        
        # Check if it is a critical deviation (data falsification)
        if re.search(r'伪造|篡改|虚假|falsif|fabricat', text):
            return Classification.CRITICAL, 0.98
        
        # Check if it is a major deviation
        if safety_impact == RiskLevel.HIGH:
            return Classification.MAJOR, 0.95
        
        if data_impact == RiskLevel.HIGH or scientific_impact == RiskLevel.HIGH:
            return Classification.MAJOR, 0.90
        
        if safety_impact == RiskLevel.MEDIUM and (
            data_impact.score >= 2 or scientific_impact.score >= 2
        ):
            return Classification.MAJOR, 0.85
        
        # Check informed consent related issues
        if re.search(r'知情同意|未获得.*同意|consent', text, re.IGNORECASE):
            if not re.search(r'非关键|轻微|延迟|delay', text, re.IGNORECASE):
                return Classification.MAJOR, 0.92
        
        # Other cases are minor deviations
        if risk_score <= 4:
            confidence = 0.90 - (risk_score * 0.05)
        else:
            confidence = 0.70
        
        return Classification.MINOR, max(0.65, confidence)
    
    def _generate_rationale(
        self,
        classification: Classification,
        safety_impact: RiskLevel,
        data_impact: RiskLevel,
        scientific_impact: RiskLevel,
        description: str
    ) -> str:
        """Generate classification rationale"""
        reasons = []
        
        if classification == Classification.CRITICAL:
            reasons.append("Involves data falsification or tampering, seriously affecting the credibility of trial data.")
        elif classification == Classification.MAJOR:
            reasons.append("This deviation has the following high-risk characteristics:")
            if safety_impact == RiskLevel.HIGH:
                reasons.append("- Seriously affects subject safety")
            if data_impact == RiskLevel.HIGH:
                reasons.append("- Seriously compromises data integrity")
            if scientific_impact == RiskLevel.HIGH:
                reasons.append("- Seriously compromises trial scientific validity")
            if safety_impact == RiskLevel.MEDIUM:
                reasons.append("- Moderate impact on subject safety")
            
            # Check informed consent
            if re.search(r'知情同意|consent', description, re.IGNORECASE):
                reasons.append("- Involves informed consent procedure violation")
        else:
            reasons.append("This deviation has the following characteristics:")
            if safety_impact == RiskLevel.NONE:
                reasons.append("- Does not affect subject safety")
            if data_impact == RiskLevel.LOW:
                reasons.append("- Minimal impact on data integrity")
            if scientific_impact == RiskLevel.NONE:
                reasons.append("- Does not affect trial scientific validity")
            
            # Check if it is a minor time delay
            if re.search(r'延迟|delay|推后|postpone', description, re.IGNORECASE):
                reasons.append("- Only a procedural delay, does not affect core trial elements")
        
        return "\n".join(reasons)
    
    def _extract_key_indicators(self, description: str, deviation_type: str) -> List[str]:
        """Extract key indicators"""
        indicators = []
        text = f"{description} {deviation_type}".lower()
        
        # Check major deviation indicators
        for category, patterns in self.major_patterns.items():
            for pattern in patterns:
                if pattern.search(text):
                    indicator_map = {
                        'informed_consent': 'Informed consent issue',
                        'eligibility': 'Inclusion/exclusion criteria violation',
                        'dosing': 'Dosing/dose issue',
                        'concomitant': 'Concomitant medication violation',
                        'randomization': 'Randomization issue',
                        'safety_reporting': 'Safety reporting issue',
                        'blinding': 'Blinding violation',
                        'data_integrity': 'Data integrity issue',
                        'critical_procedures': 'Critical procedure omission'
                    }
                    ind = indicator_map.get(category, category)
                    if ind not in indicators:
                        indicators.append(ind)
                    break
        
        # Check minor deviation indicators
        for category, patterns in self.minor_patterns.items():
            for pattern in patterns:
                if pattern.search(text):
                    indicator_map = {
                        'visit_window': 'Visit window deviation',
                        'sample_collection': 'Sample collection deviation',
                        'questionnaire': 'Questionnaire/diary card deviation',
                        'documentation': 'Documentation/signature delay',
                        'non_critical': 'Non-critical procedure deviation'
                    }
                    ind = indicator_map.get(category, category)
                    if ind not in indicators:
                        indicators.append(ind)
                    break
        
        return indicators[:5]  # Return at most 5 indicators
    
    def _get_regulatory_basis(self, classification: Classification, description: str) -> List[str]:
        """Get regulatory basis"""
        basis = []
        text = description.lower()
        
        if classification == Classification.CRITICAL:
            basis = self.REGULATORY_BASIS['critical'].copy()
        elif classification == Classification.MAJOR:
            basis = self.REGULATORY_BASIS['major'].copy()
            
            # Add specific regulations based on description
            if re.search(r'知情同意|consent', text, re.IGNORECASE):
                basis.append("ICH E6(R2) Section 4.8 - Informed Consent Requirements")
            if re.search(r'随机化|randomiz', text, re.IGNORECASE):
                basis.append("ICH E9 - Statistical Principles for Clinical Trials")
        else:
            basis = self.REGULATORY_BASIS['minor'].copy()
        
        return basis
    
    def _get_recommended_actions(self, classification: Classification) -> List[str]:
        """Get recommended actions"""
        if classification == Classification.CRITICAL:
            return [
                "Immediately notify sponsor and ethics committee",
                "Initiate root cause investigation",
                "Implement corrective and preventive actions (CAPA)",
                "Consider blacklisting the investigator",
                "Assess impact on overall trial data"
            ]
        elif classification == Classification.MAJOR:
            return [
                "Document in deviation log",
                "Report to sponsor within 24 hours",
                "Report to ethics committee (if required by protocol)",
                "Assess whether remedial action is needed",
                "Track trends, assess if it is a systemic issue"
            ]
        else:
            return [
                "Document in deviation log",
                "Track trends",
                "Resolve at site level",
                "Periodic summary reporting (e.g. quarterly)"
            ]
    
    def _generate_event_id(self) -> str:
        """Generate event ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"DEV-{timestamp}"
    
    def generate_report(self, results: List[ClassificationResult]) -> Dict:
        """
        Generate deviation classification report
        
        Args:
            results: List of classification results
        
        Returns:
            Dict: Report dictionary
        """
        if not results:
            return {"error": "No results to report"}
        
        total = len(results)
        major_count = sum(1 for r in results if r.classification == Classification.MAJOR)
        minor_count = sum(1 for r in results if r.classification == Classification.MINOR)
        critical_count = sum(1 for r in results if r.classification == Classification.CRITICAL)
        
        # Summarize deviations by category
        by_category = {}
        for result in results:
            for indicator in result.key_indicators:
                by_category[indicator] = by_category.get(indicator, 0) + 1
        
        return {
            "report_date": datetime.now().isoformat(),
            "summary": {
                "total_deviations": total,
                "critical_count": critical_count,
                "major_count": major_count,
                "minor_count": minor_count,
                "major_rate": round(major_count / total * 100, 1) if total > 0 else 0,
                "minor_rate": round(minor_count / total * 100, 1) if total > 0 else 0
            },
            "category_breakdown": by_category,
            "critical_deviations": [
                r.to_dict() for r in results 
                if r.classification == Classification.CRITICAL
            ],
            "major_deviations": [
                r.to_dict() for r in results 
                if r.classification == Classification.MAJOR
            ],
            "minor_deviations": [
                r.to_dict() for r in results 
                if r.classification == Classification.MINOR
            ],
            "recommendations": self._generate_summary_recommendations(results)
        }
    
    def _generate_summary_recommendations(self, results: List[ClassificationResult]) -> List[str]:
        """Generate summary recommendations"""
        recommendations = []
        
        critical_count = sum(1 for r in results if r.classification == Classification.CRITICAL)
        major_count = sum(1 for r in results if r.classification == Classification.MAJOR)
        total = len(results)
        
        if critical_count > 0:
            recommendations.append(
                f"WARNING: {critical_count} critical deviation(s) found, immediate root cause analysis recommended"
            )
        
        if total > 0:
            major_rate = major_count / total * 100
            if major_rate > 20:
                recommendations.append(
                    f"Major deviation rate ({major_rate:.1f}%) is high, recommend strengthening site training"
                )
            elif major_rate > 10:
                recommendations.append(
                    f"Major deviation rate ({major_rate:.1f}%) is moderate, recommend close monitoring"
                )
        
        # Check trends
        safety_issues = sum(
            1 for r in results 
            if r.safety_risk in [RiskLevel.HIGH, RiskLevel.MEDIUM]
        )
        if safety_issues > 3:
            recommendations.append(
                f"{safety_issues} deviation(s) involving safety issues found, recommend evaluating subject protection measures"
            )
        
        if not recommendations:
            recommendations.append("Overall deviation control is good, recommend maintaining current standards")
        
        return recommendations


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Protocol Deviation Classifier - Clinical trial protocol deviation classification tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Classify a single deviation
  python scripts/main.py classify -d "Subject visit delayed by 2 days"
  
  # Batch classify from file
  python scripts/main.py batch -i deviations.json -o report.json
  
  # Interactive classification
  python scripts/main.py interactive
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # classify command
    classify_parser = subparsers.add_parser("classify", help="Classify a single deviation")
    classify_parser.add_argument("-d", "--description", required=True, help="Deviation description")
    classify_parser.add_argument("-t", "--type", default="", help="Deviation type")
    classify_parser.add_argument("--id", default="", help="Event ID")
    classify_parser.add_argument("--safety-impact", 
                                 choices=["none", "low", "medium", "high"],
                                 default="none", help="Safety impact level")
    classify_parser.add_argument("--data-impact",
                                 choices=["none", "low", "medium", "high"],
                                 default="low", help="Data integrity impact level")
    classify_parser.add_argument("--scientific-impact",
                                 choices=["none", "low", "medium", "high"],
                                 default="none", help="Scientific validity impact level")
    classify_parser.add_argument("-o", "--output", choices=["json", "table"], 
                                 default="table", help="Output format")
    
    # batch command
    batch_parser = subparsers.add_parser("batch", help="Batch classification")
    batch_parser.add_argument("-i", "--input", required=True, help="Input JSON file path")
    batch_parser.add_argument("-o", "--output", default="", help="Output file path")
    batch_parser.add_argument("--format", choices=["json", "report"],
                              default="json", help="Output format")
    
    # report command
    report_parser = subparsers.add_parser("report", help="Generate summary report")
    report_parser.add_argument("-i", "--input", required=True, help="Classification result JSON file")
    
    # interactive command
    subparsers.add_parser("interactive", help="Interactive classification")
    
    # demo command
    subparsers.add_parser("demo", help="Run sample classification")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    classifier = DeviationClassifier()
    
    try:
        if args.command == "classify":
            # Parse impact levels
            safety = RiskLevel(args.safety_impact)
            data = RiskLevel(args.data_impact)
            scientific = RiskLevel(args.scientific_impact)
            
            result = classifier.classify(
                description=args.description,
                deviation_type=args.type,
                event_id=args.id,
                safety_impact=safety,
                data_impact=data,
                scientific_impact=scientific
            )
            
            if args.output == "json":
                print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
            else:
                _print_table_result(result)
        
        elif args.command == "batch":
            # Read input file
            with open(args.input, 'r', encoding='utf-8') as f:
                events = json.load(f)
            
            results = classifier.classify_batch(events)
            
            if args.format == "report":
                report = classifier.generate_report(results)
                output = report
            else:
                output = [r.to_dict() for r in results]
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(output, f, ensure_ascii=False, indent=2)
                print(f"Results saved to: {args.output}")
            else:
                print(json.dumps(output, ensure_ascii=False, indent=2))
        
        elif args.command == "report":
            with open(args.input, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Assume input is a list of classification results
            if isinstance(data, list):
                # Convert to ClassificationResult objects
                results = []
                for item in data:
                    result = ClassificationResult(
                        id=item.get('id', ''),
                        classification=Classification(item.get('classification_en', '').lower().split()[0]),
                        confidence=item.get('confidence', 0),
                        rationale=item.get('rationale', ''),
                        safety_risk=RiskLevel.NONE,
                        data_integrity_risk=RiskLevel.NONE,
                        scientific_validity_risk=RiskLevel.NONE,
                        risk_score=item.get('risk_score', 0),
                        regulatory_basis=item.get('regulatory_basis', []),
                        recommended_actions=item.get('recommended_actions', []),
                        key_indicators=item.get('key_indicators', [])
                    )
                    results.append(result)
                
                report = classifier.generate_report(results)
                print(json.dumps(report, ensure_ascii=False, indent=2))
        
        elif args.command == "interactive":
            _run_interactive(classifier)
        
        elif args.command == "demo":
            _run_demo(classifier)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _print_table_result(result: ClassificationResult):
    """Print result in table format"""
    print("\n" + "=" * 60)
    print("Protocol Deviation Classification Result")
    print("=" * 60)
    print(f"{'Event ID:':<20} {result.id}")
    print(f"{'Classification:':<20} {result.classification} ({result.classification.en_name})")
    print(f"{'Confidence:':<20} {result.confidence*100:.1f}%")
    print(f"{'Risk Score:':<20} {result.risk_score}")
    print("-" * 60)
    print("Risk Assessment:")
    print(f"  - Subject Safety: {result.safety_risk}")
    print(f"  - Data Integrity: {result.data_integrity_risk}")
    print(f"  - Trial Scientific Validity: {result.scientific_validity_risk}")
    print("-" * 60)
    print("Classification Rationale:")
    print(result.rationale)
    if result.key_indicators:
        print("-" * 60)
        print("Key Indicators:")
        for indicator in result.key_indicators:
            print(f"  • {indicator}")
    print("-" * 60)
    print("Recommended Actions:")
    for action in result.recommended_actions:
        print(f"  • {action}")
    print("=" * 60)


def _run_interactive(classifier: DeviationClassifier):
    """Run interactive classification"""
    print("\n" + "=" * 60)
    print("Protocol Deviation Classifier - Interactive Mode")
    print("=" * 60)
    print("Enter 'quit' or 'q' to exit\n")
    
    while True:
        print("\n" + "-" * 40)
        description = input("Please enter deviation description: ").strip()
        
        if description.lower() in ['quit', 'q', 'exit']:
            print("Goodbye!")
            break
        
        if not description:
            print("Description cannot be empty, please re-enter.")
            continue
        
        deviation_type = input("Please enter deviation type (optional): ").strip()
        
        print("\nAnalyzing...")
        result = classifier.classify(
            description=description,
            deviation_type=deviation_type
        )
        
        _print_table_result(result)


def _run_demo(classifier: DeviationClassifier):
    """Run sample classification"""
    demo_cases = [
        {
            "id": "DEV-001",
            "description": "Subject visit delayed by 2 days",
            "type": "Visit Window"
        },
        {
            "id": "DEV-002",
            "description": "Blood sample collected without obtaining informed consent",
            "type": "Informed Consent"
        },
        {
            "id": "DEV-003",
            "description": "Subject accidentally took double dose of study medication",
            "type": "Dosing Error"
        },
        {
            "id": "DEV-004",
            "description": "Quality of life questionnaire submitted 3 days late",
            "type": "Data Collection"
        },
        {
            "id": "DEV-005",
            "description": "Subject not meeting inclusion criteria was enrolled (age out of range)",
            "type": "Inclusion Criteria"
        }
    ]
    
    print("\n" + "=" * 60)
    print("Protocol Deviation Classifier - Demo Run")
    print("=" * 60)
    
    results = []
    for case in demo_cases:
        print(f"\n[Case {case['id']}]")
        print(f"Description: {case['description']}")
        print(f"Type: {case['type']}")
        
        result = classifier.classify(
            description=case['description'],
            deviation_type=case['type'],
            event_id=case['id']
        )
        results.append(result)
        
        print(f"-> Classification: {result.classification} (Confidence: {result.confidence*100:.0f}%)")
        print(f"   Risk Score: {result.risk_score}")
    
    # Generate summary report
    print("\n" + "=" * 60)
    print("Summary Report")
    print("=" * 60)
    
    report = classifier.generate_report(results)
    summary = report['summary']
    
    print(f"Total Deviations: {summary['total_deviations']}")
    print(f"Critical Deviations: {summary['critical_count']}")
    print(f"Major Deviations: {summary['major_count']} ({summary['major_rate']}%)")
    print(f"Minor Deviations: {summary['minor_count']} ({summary['minor_rate']}%)")
    
    print("\nRecommendations:")
    for rec in report['recommendations']:
        print(f"  • {rec}")


if __name__ == "__main__":
    main()
