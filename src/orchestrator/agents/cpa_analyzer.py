"""
CPA Analysis Agent - Identifies reasons for high CPA and suggests optimizations
"""
from src.orchestrator.utils.model import call_model
from src.orchestrator.utils.io_utils import load_prompt
import json


class CPAAnalyzer:
    """Analyzes Meta Ads data to identify high CPA root causes and recommend optimizations"""

    def run(self, data):
        """
        Analyze CPA metrics and provide optimization recommendations
        
        Args:
            data: List of dicts with spend, impressions, clicks, conversions, revenue
            
        Returns:
            dict with CPA analysis and optimization strategies
        """
        cpa_metrics = self._calculate_cpa_metrics(data)
        root_causes = self._identify_root_causes(cpa_metrics)
        optimizations = self._generate_optimizations(cpa_metrics, root_causes)
        
        return {
            "cpa_metrics": cpa_metrics,
            "root_causes": root_causes,
            "optimization_strategies": optimizations,
            "priority_actions": self._prioritize_actions(optimizations)
        }

    def _calculate_cpa_metrics(self, data):
        """Calculate CPA and related metrics"""
        metrics = []
        
        for record in data:
            spend = float(record.get('spend', 0))
            impressions = float(record.get('impressions', 0))
            clicks = float(record.get('clicks', 0))
            conversions = float(record.get('conversions', 0))
            revenue = float(record.get('revenue', 0))
            
            # Calculate key metrics
            cpa = spend / conversions if conversions > 0 else float('inf')
            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            cpc = (spend / clicks) if clicks > 0 else 0
            cpm = (spend / impressions * 1000) if impressions > 0 else 0
            conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
            roas = revenue / spend if spend > 0 else 0
            
            metrics.append({
                "date": record.get('date', 'N/A'),
                "spend": spend,
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "revenue": revenue,
                "cpa": round(cpa, 2),
                "ctr": round(ctr, 2),
                "cpc": round(cpc, 2),
                "cpm": round(cpm, 2),
                "conversion_rate": round(conversion_rate, 2),
                "roas": round(roas, 2)
            })
        
        return metrics

    def _identify_root_causes(self, metrics):
        """Identify root causes of high CPA"""
        causes = []
        
        if not metrics:
            return causes
        
        avg_cpa = sum(m['cpa'] for m in metrics if m['cpa'] != float('inf')) / len(
            [m for m in metrics if m['cpa'] != float('inf')]
        ) if any(m['cpa'] != float('inf') for m in metrics) else 0
        
        avg_conversion_rate = sum(m['conversion_rate'] for m in metrics) / len(metrics)
        avg_ctr = sum(m['ctr'] for m in metrics) / len(metrics)
        avg_cpc = sum(m['cpc'] for m in metrics) / len(metrics)
        
        # Root cause analysis
        if avg_conversion_rate < 2:
            causes.append({
                "cause": "Low Conversion Rate",
                "current": f"{avg_conversion_rate:.2f}%",
                "benchmark": "2-5%",
                "impact": "HIGH",
                "explanation": "Low conversion rate is the primary driver of high CPA. Even with good traffic, few visitors convert."
            })
        
        if avg_ctr < 1:
            causes.append({
                "cause": "Low Click-Through Rate",
                "current": f"{avg_ctr:.2f}%",
                "benchmark": "0.5-2%",
                "impact": "MEDIUM",
                "explanation": "Low CTR indicates weak ad creatives or poor audience targeting. More clicks needed for efficient conversion optimization."
            })
        
        if avg_cpc > 2:
            causes.append({
                "cause": "High Cost Per Click",
                "current": f"${avg_cpc:.2f}",
                "benchmark": "$0.50-$2.00",
                "impact": "MEDIUM",
                "explanation": "High CPC increases baseline cost, making CPA harder to optimize. Review bidding strategy and competition."
            })
        
        # Quality score assessment
        if avg_ctr < 0.5 and avg_cpc > 1:
            causes.append({
                "cause": "Poor Ad Quality/Relevance",
                "current": "CTR < 0.5%, CPC > $1",
                "benchmark": "CTR > 1%, CPC < $1",
                "impact": "HIGH",
                "explanation": "Meta's algorithm penalizes low-quality ads with higher costs. Ad relevance or landing page quality may be poor."
            })
        
        # Audience issues
        if len(metrics) > 1:
            conversion_variance = max(m['conversion_rate'] for m in metrics) - min(m['conversion_rate'] for m in metrics)
            if conversion_variance > 3:
                causes.append({
                    "cause": "Inconsistent Performance / Poor Audience Segmentation",
                    "current": f"Conversion rate variance: {conversion_variance:.2f}%",
                    "benchmark": "< 1% variance",
                    "impact": "MEDIUM",
                    "explanation": "High variability suggests mixed audience quality. Segment audiences by demographics, interests, or behaviors."
                })
        
        return causes

    def _generate_optimizations(self, metrics, root_causes):
        """Generate optimization strategies based on root causes"""
        optimizations = []
        
        # Always include these fundamental optimizations
        optimizations.append({
            "priority": "CRITICAL",
            "strategy": "Landing Page Optimization",
            "tactics": [
                "Ensure landing page matches ad copy and creative",
                "Reduce load time to < 3 seconds",
                "Simplify conversion funnel (1-step checkout preferred)",
                "Add trust signals (testimonials, security badges, social proof)",
                "Mobile-optimize: 60%+ of traffic is mobile"
            ],
            "expected_impact": "20-40% CPA reduction",
            "timeline": "1-2 weeks"
        })
        
        optimizations.append({
            "priority": "CRITICAL",
            "strategy": "Audience Segmentation & Refinement",
            "tactics": [
                "Create lookalike audiences from high-converting customers",
                "Exclude low-value audience segments",
                "Focus on warm audiences first (website visitors, email list)",
                "Test narrower interest combinations for better relevance",
                "Use Custom Audiences with purchase intent signals"
            ],
            "expected_impact": "15-35% CPA reduction",
            "timeline": "2-3 weeks"
        })
        
        optimizations.append({
            "priority": "CRITICAL",
            "strategy": "Creative Refresh & Testing",
            "tactics": [
                "Test 5+ ad variations (different copy, visuals, hooks)",
                "Use video creatives (25% higher conversion than static)",
                "A/B test headlines: benefit-driven vs curiosity-driven",
                "Test carousel ads to showcase product variety",
                "Leverage user-generated content for authenticity"
            ],
            "expected_impact": "10-25% CPA reduction",
            "timeline": "1-2 weeks"
        })
        
        optimizations.append({
            "priority": "HIGH",
            "strategy": "Bidding Strategy Optimization",
            "tactics": [
                "Switch to CPA-based bidding (Lowest Cost w/ CPA cap)",
                "Set realistic CPA target based on business margins",
                "Allow 1-2 week learning period before adjusting",
                "Use Advantage+ campaigns for better optimization",
                "Test different bid caps: start at 50% above current CPA"
            ],
            "expected_impact": "10-20% CPA reduction",
            "timeline": "3-7 days for implementation"
        })
        
        optimizations.append({
            "priority": "HIGH",
            "strategy": "Conversion Event Optimization",
            "tactics": [
                "Ensure Pixel is tracking ALL conversions (don't rely on Purchase only)",
                "Use lower-funnel events: Add to Cart, Initiate Checkout",
                "Implement server-side tracking for improved accuracy",
                "Verify conversion values are correctly attributed",
                "Check for pixel fires on all conversion pages"
            ],
            "expected_impact": "5-15% CPA improvement through better optimization",
            "timeline": "1 week"
        })
        
        optimizations.append({
            "priority": "MEDIUM",
            "strategy": "Dayparting & Schedule Optimization",
            "tactics": [
                "Analyze performance by day of week and time of day",
                "Increase budget during peak conversion windows",
                "Reduce spend during low-performing hours",
                "Test geographic targeting adjustments",
                "Consider timezone differences for global campaigns"
            ],
            "expected_impact": "5-10% CPA reduction",
            "timeline": "1-2 weeks (requires data)"
        })
        
        optimizations.append({
            "priority": "MEDIUM",
            "strategy": "Retargeting Strategy",
            "tactics": [
                "Create retargeting campaign for site visitors (1-7 day window)",
                "Target add-to-cart abandoners with cart recovery ads",
                "Use dynamic product ads to remind users of viewed items",
                "Offer incentives (10-15% discount) to previous visitors",
                "Segment by recency: recent vs older visitors"
            ],
            "expected_impact": "20-40% lower CPA for retargeting",
            "timeline": "1 week"
        })
        
        return optimizations

    def _prioritize_actions(self, optimizations):
        """Create prioritized action plan"""
        actions = []
        
        critical = [o for o in optimizations if o['priority'] == 'CRITICAL']
        high = [o for o in optimizations if o['priority'] == 'HIGH']
        
        week_1 = critical[:2] + high[:1]
        week_2 = critical[2:] + high[1:]
        
        return {
            "immediate_actions_week1": [
                {
                    "action": "Landing Page Audit",
                    "owner": "Product/Marketing",
                    "checklist": [
                        "Load time test",
                        "Mobile responsiveness check",
                        "Conversion funnel analysis",
                        "Copy relevance to ads review"
                    ]
                },
                {
                    "action": "Launch Creative A/B Test",
                    "owner": "Creative Team",
                    "checklist": [
                        "Create 5 ad variations",
                        "Set 50/50 budget split",
                        "Define clear performance metrics",
                        "Schedule results review"
                    ]
                },
                {
                    "action": "Validate Meta Pixel Installation",
                    "owner": "Technical/Data Team",
                    "checklist": [
                        "Verify pixel fires on all conversion pages",
                        "Check event mapping accuracy",
                        "Validate conversion value tracking",
                        "Enable server-side tracking if possible"
                    ]
                }
            ],
            "week_2_actions": [
                {
                    "action": "Audience Segmentation",
                    "owner": "Data/Analytics",
                    "checklist": [
                        "Create lookalike audiences",
                        "Build warm audience segments",
                        "Set exclusion lists",
                        "Test audience combinations"
                    ]
                },
                {
                    "action": "Optimize Bidding Strategy",
                    "owner": "Paid Media",
                    "checklist": [
                        "Switch to Lowest Cost CPA bidding",
                        "Set realistic CPA cap",
                        "Configure bid escalation schedule",
                        "Monitor daily performance"
                    ]
                }
            ],
            "ongoing_monitoring": [
                "Daily: Monitor CPA, ROAS, conversion rate",
                "Weekly: Review A/B test results, adjust top performers",
                "Bi-weekly: Analyze audience performance trends",
                "Monthly: Full campaign review and optimization recommendations"
            ]
        }
