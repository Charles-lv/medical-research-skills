#!/usr/bin/env python3
"""
Toxicity Structure Alert (Skill ID: 141)
Scans drug molecular structures to identify potential toxicity alert structures.

Usage:
    python main.py --input <smiles> [--format json|text] [--detail level]
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from enum import Enum


class RiskLevel(Enum):
    """Risk level"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass
class ToxicAlert:
    """Toxicity alert structure data class"""
    name: str
    name_en: str
    type: str
    smarts: str
    risk_level: RiskLevel
    description: str
    weight: float = 1.0


@dataclass
class AlertMatch:
    """Matched alert"""
    name: str
    type: str
    smarts: str
    risk_level: str
    description: str
    match_count: int = 1


@dataclass
class ScanResult:
    """Scan result"""
    input_smiles: str
    mol_weight: Optional[float]
    alert_count: int
    risk_score: float
    risk_level: str
    alerts: List[AlertMatch]
    recommendations: List[str]


class ToxicityAlertScanner:
    """Toxicity alert structure scanner"""
    
    # Predefined toxicity alert structures
    TOXIC_ALERTS = [
        # High toxicity alerts
        ToxicAlert(
            name="Aromatic Nitro",
            name_en="Aromatic Nitro",
            type="mutagenic",
            smarts="[N+](=O)[O-]c",
            risk_level=RiskLevel.HIGH,
            description="Nitroaromatic compounds may cause DNA damage with mutagenic and potential carcinogenic properties",
            weight=1.0
        ),
        ToxicAlert(
            name="Aromatic Primary Amine",
            name_en="Aromatic Primary Amine",
            type="carcinogenic",
            smarts="Nc1ccccc1",
            risk_level=RiskLevel.HIGH,
            description="Aromatic amines can be metabolically activated to produce electrophilic species that form adducts with DNA",
            weight=0.9
        ),
        ToxicAlert(
            name="Epoxide",
            name_en="Epoxide",
            type="alkylating",
            smarts="C1OC1",
            risk_level=RiskLevel.HIGH,
            description="Epoxides are highly reactive three-membered ring ethers that can act as alkylating agents to damage DNA",
            weight=1.0
        ),
        ToxicAlert(
            name="Aziridine",
            name_en="Aziridine",
            type="alkylating",
            smarts="C1NC1",
            risk_level=RiskLevel.HIGH,
            description="Aziridine rings are highly reactive and can act as alkylating agents",
            weight=1.0
        ),
        ToxicAlert(
            name="Hydrazine",
            name_en="Hydrazine",
            type="hepatotoxic",
            smarts="[NX3][NX3]",
            risk_level=RiskLevel.HIGH,
            description="Hydrazine compounds are hepatotoxic and may cause liver damage",
            weight=0.9
        ),
        ToxicAlert(
            name="Haloalkyl",
            name_en="Haloalkyl",
            type="alkylating",
            smarts="[C][F,Cl,Br,I]",
            risk_level=RiskLevel.HIGH,
            description="Haloalkyl groups can serve as leaving groups, forming electrophilic centers that cause alkylation",
            weight=0.85
        ),
        ToxicAlert(
            name="Polycyclic Aromatic Hydrocarbon",
            name_en="Polycyclic Aromatic Hydrocarbon",
            type="carcinogenic",
            smarts="c1ccc2c(c1)ccc1c3ccccc3ccc21",
            risk_level=RiskLevel.HIGH,
            description="PAHs can be metabolically activated to form carcinogenic epoxides",
            weight=0.95
        ),
        
        # Medium toxicity alerts
        ToxicAlert(
            name="Aldehyde",
            name_en="Aldehyde",
            type="reactive",
            smarts="[CX3H1](=O)",
            risk_level=RiskLevel.MEDIUM,
            description="Aldehydes are electrophilic and can form Schiff bases with proteins",
            weight=0.6
        ),
        ToxicAlert(
            name="Acyl Chloride",
            name_en="Acyl Chloride",
            type="reactive",
            smarts="C(=O)Cl",
            risk_level=RiskLevel.MEDIUM,
            description="Acyl chlorides are highly reactive and can undergo acylation with nucleophilic groups",
            weight=0.7
        ),
        ToxicAlert(
            name="Michael Acceptor",
            name_en="Michael Acceptor",
            type="electrophilic",
            smarts="C=CC(=O)",
            risk_level=RiskLevel.MEDIUM,
            description="Alpha,beta-unsaturated carbonyl groups can act as Michael acceptors and covalently bind to thiol groups",
            weight=0.65
        ),
        ToxicAlert(
            name="Quinone",
            name_en="Quinone",
            type="oxidative",
            smarts="O=C1C=CC(=O)C=C1",
            risk_level=RiskLevel.MEDIUM,
            description="Quinones can generate reactive oxygen species through redox cycling, causing oxidative stress",
            weight=0.7
        ),
        ToxicAlert(
            name="Nitroso",
            name_en="Nitroso",
            type="carcinogenic",
            smarts="N=O",
            risk_level=RiskLevel.MEDIUM,
            description="N-nitroso compounds have potential carcinogenicity",
            weight=0.75
        ),
        ToxicAlert(
            name="Thioester",
            name_en="Thioester",
            type="reactive",
            smarts="C(=O)S",
            risk_level=RiskLevel.MEDIUM,
            description="Thioesters can undergo exchange reactions with thiol groups",
            weight=0.55
        ),
        
        # Low toxicity alerts
        ToxicAlert(
            name="Thiol",
            name_en="Thiol",
            type="reactive",
            smarts="[SX2H]",
            risk_level=RiskLevel.LOW,
            description="Thiols are reactive and can participate in redox reactions and metal chelation",
            weight=0.3
        ),
        ToxicAlert(
            name="Sulfonyl Chloride",
            name_en="Sulfonyl Chloride",
            type="reactive",
            smarts="S(=O)(=O)Cl",
            risk_level=RiskLevel.LOW,
            description="Sulfonyl chlorides can react with nucleophiles",
            weight=0.4
        ),
    ]
    
    def __init__(self):
        self.alerts = self.TOXIC_ALERTS
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile SMARTS patterns"""
        try:
            from rdkit import Chem
            self.has_rdkit = True
            self._compiled_patterns = {}
            for alert in self.alerts:
                try:
                    pattern = Chem.MolFromSmarts(alert.smarts)
                    if pattern:
                        self._compiled_patterns[alert.name] = pattern
                except Exception:
                    pass
        except ImportError:
            self.has_rdkit = False
            print("Warning: RDKit not available. Falling back to basic pattern matching.", file=sys.stderr)
    
    def _parse_smiles(self, smiles: str) -> Tuple[Optional['Chem.Mol'], Optional[float]]:
        """Parse SMILES string"""
        if not self.has_rdkit:
            return None, None
        
        from rdkit import Chem
        from rdkit.Chem import Descriptors
        
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None, None
        
        mol_weight = Descriptors.MolWt(mol)
        return mol, mol_weight
    
    def _match_alerts(self, mol) -> List[AlertMatch]:
        """Match toxicity alert structures"""
        matches = []
        
        if self.has_rdkit and mol is not None:
            # Use RDKit for precise substructure matching
            from rdkit import Chem
            for alert in self.alerts:
                pattern = self._compiled_patterns.get(alert.name)
                if pattern:
                    try:
                        match_list = mol.GetSubstructMatches(pattern)
                        if match_list:
                            matches.append(AlertMatch(
                                name=alert.name,
                                type=alert.type,
                                smarts=alert.smarts,
                                risk_level=alert.risk_level.value,
                                description=alert.description,
                                match_count=len(match_list)
                            ))
                    except Exception:
                        pass
        else:
            # Fallback mode: use simple string matching
            smiles_upper = self._current_smiles.upper()
            matches = self._fallback_string_match(smiles_upper)
        
        return matches
    
    def _fallback_string_match(self, smiles: str) -> List[AlertMatch]:
        """Fallback mode: simple string pattern matching"""
        matches = []
        
        # Define simplified pattern strings
        fallback_patterns = {
            "Aromatic Nitro": ("O=[N+]([O-])", "NO2"),
            "Aromatic Primary Amine": ("NC", "NH2"),
            "Epoxide": ("C1OC1",),
            "Aziridine": ("C1NC1",),
            "Hydrazine": ("NN",),
            "Haloalkyl": ("CL", "BR", "F", "I"),
            "Polycyclic Aromatic Hydrocarbon": ("C=CC=CC=CC=CC",),
            "Aldehyde": ("C=O", "CHO"),
            "Acyl Chloride": ("C(=O)CL", "COCL"),
            "Michael Acceptor": ("C=CC=O",),
            "Quinone": ("O=C1C=CC(=O)",),
            "Nitroso": ("N=O", "N-O"),
            "Thiol": ("SH",),
        }
        
        alert_map = {a.name: a for a in self.alerts}
        matched_names = set()
        
        for alert_name, patterns in fallback_patterns.items():
            if alert_name in matched_names:
                continue
            for pattern in patterns:
                if pattern in smiles:
                    alert = alert_map.get(alert_name)
                    if alert:
                        matches.append(AlertMatch(
                            name=alert.name,
                            type=alert.type,
                            smarts=alert.smarts,
                            risk_level=alert.risk_level.value,
                            description=alert.description,
                            match_count=smiles.count(pattern)
                        ))
                        matched_names.add(alert_name)
                        break
        
        return matches
    
    def _calculate_risk_score(self, matches: List[AlertMatch]) -> Tuple[float, str]:
        """Calculate risk score and level"""
        if not matches:
            return 0.0, "NONE"
        
        # Get weights for matched alerts
        alert_weights = {a.name: (a.weight, a.risk_level) for a in self.alerts}
        
        total_weight = 0.0
        max_risk = RiskLevel.LOW
        
        for match in matches:
            weight, risk = alert_weights.get(match.name, (0.3, RiskLevel.LOW))
            total_weight += weight * match.match_count
            
            if risk == RiskLevel.HIGH:
                max_risk = RiskLevel.HIGH
            elif risk == RiskLevel.MEDIUM and max_risk != RiskLevel.HIGH:
                max_risk = RiskLevel.MEDIUM
        
        # Calculate risk score (0-1)
        risk_score = min(total_weight / 2.0, 1.0)
        
        return round(risk_score, 2), max_risk.value
    
    def _generate_recommendations(self, matches: List[AlertMatch], risk_level: str) -> List[str]:
        """Generate recommendations"""
        recommendations = []
        
        if risk_level == "HIGH":
            recommendations.append("⚠️ High-risk toxicity structures detected; strongly recommend Ames test validation")
            recommendations.append("⚠️ Consider structural optimization to reduce potential toxicity risk")
        elif risk_level == "MEDIUM":
            recommendations.append("⚡ Medium-risk structures detected; recommend in vitro toxicity screening")
            recommendations.append("⚡ Evaluate the impact of structural modifications on activity and toxicity")
        
        # Provide recommendations based on specific alert types
        alert_types = set(m.type for m in matches)
        
        if "mutagenic" in alert_types or "carcinogenic" in alert_types:
            recommendations.append("🧬 Recommend mutagenicity assessment (e.g., Ames test, chromosomal aberration assay)")
        if "hepatotoxic" in alert_types:
            recommendations.append("🫀 Recommend hepatotoxicity risk assessment")
        if "alkylating" in alert_types:
            recommendations.append("⚗️ Alkylating agents have high reactivity; pay special attention to off-target effects")
        if "reactive" in alert_types:
            recommendations.append("🔄 Reactive groups may affect metabolic stability; recommend plasma stability assessment")
        
        if not recommendations:
            recommendations.append("✅ No significant toxicity alert structures detected, but standard safety assessment is still recommended")
        
        return recommendations
    
    def scan(self, smiles: str) -> ScanResult:
        """
        Scan a SMILES string to identify toxicity alert structures
        
        Args:
            smiles: Input SMILES string
            
        Returns:
            ScanResult: Scan result
        """
        self._current_smiles = smiles  # Save for fallback mode
        mol, mol_weight = self._parse_smiles(smiles)
        matches = self._match_alerts(mol)
        risk_score, risk_level = self._calculate_risk_score(matches)
        recommendations = self._generate_recommendations(matches, risk_level)
        
        return ScanResult(
            input_smiles=smiles,
            mol_weight=round(mol_weight, 2) if mol_weight else None,
            alert_count=len(matches),
            risk_score=risk_score,
            risk_level=risk_level,
            alerts=matches,
            recommendations=recommendations
        )
    
    def format_text_output(self, result: ScanResult, detail: str = "standard") -> str:
        """Format text output"""
        lines = []
        lines.append("=" * 60)
        lines.append("     Toxicity Structure Alert Scan Report")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"Input SMILES: {result.input_smiles}")
        if result.mol_weight:
            lines.append(f"Molecular Weight: {result.mol_weight} Da")
        lines.append("")
        
        # Risk level display
        risk_emojis = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢", "NONE": "✅"}
        risk_emoji = risk_emojis.get(result.risk_level, "⚪")
        lines.append(f"Risk Level: {risk_emoji} {result.risk_level}")
        lines.append(f"Risk Score: {result.risk_score:.2f} / 1.0")
        lines.append(f"Alert Count: {result.alert_count}")
        lines.append("")
        
        if result.alerts:
            lines.append("-" * 60)
            lines.append("Detected Alert Structures:")
            lines.append("-" * 60)
            for i, alert in enumerate(result.alerts, 1):
                lines.append(f"\n{i}. {alert.name}")
                lines.append(f"   Type: {alert.type}")
                lines.append(f"   Risk: {alert.risk_level}")
                if detail in ("standard", "full"):
                    lines.append(f"   SMARTS: {alert.smarts}")
                if detail == "full":
                    lines.append(f"   Description: {alert.description}")
                if alert.match_count > 1:
                    lines.append(f"   Match Count: {alert.match_count}")
        
        lines.append("")
        lines.append("-" * 60)
        lines.append("Recommendations:")
        lines.append("-" * 60)
        for rec in result.recommendations:
            lines.append(f"  {rec}")
        
        lines.append("")
        lines.append("=" * 60)
        lines.append("Note: This tool is based on known alert structures and cannot replace comprehensive toxicological assessment")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def format_json_output(self, result: ScanResult) -> str:
        """Format JSON output"""
        data = {
            "input": result.input_smiles,
            "mol_weight": result.mol_weight,
            "alert_count": result.alert_count,
            "risk_score": result.risk_score,
            "risk_level": result.risk_level,
            "alerts": [
                {
                    "name": a.name,
                    "type": a.type,
                    "smarts": a.smarts,
                    "risk_level": a.risk_level,
                    "description": a.description,
                    "match_count": a.match_count
                }
                for a in result.alerts
            ],
            "recommendations": result.recommendations
        }
        return json.dumps(data, ensure_ascii=False, indent=2)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Toxicity Structure Alert - Scan drug molecular structures for toxicity alerts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -i "O=[N+]([O-])c1ccccc1"
  python main.py -i "C1CCCCC1" -f json
  python main.py -i "c1ccc2c(c1)ccc1c3ccccc3ccc21" -d full
        """
    )
    
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input SMILES string"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "--detail", "-d",
        choices=["basic", "standard", "full"],
        default="standard",
        help="Detail level (default: standard)"
    )
    
    args = parser.parse_args()
    
    # Create scanner and run scan
    scanner = ToxicityAlertScanner()
    result = scanner.scan(args.input)
    
    # Output result
    if args.format == "json":
        print(scanner.format_json_output(result))
    else:
        print(scanner.format_text_output(result, args.detail))
    
    # Return non-zero exit code if high risk is detected
    if result.risk_level == "HIGH":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
