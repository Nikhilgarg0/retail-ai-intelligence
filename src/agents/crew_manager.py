# src/agents/crew_manager.py
from crewai import Agent, Task, Crew, Process, LLM
from config.settings import settings
from typing import List, Dict
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RetailIntelligenceCrew:
    """Multi-agent system for comprehensive retail analysis"""
    
    def __init__(self):
        """Initialize CrewAI with Groq LLM"""
        # Configure LLM for all agents to use Groq
        self.llm = LLM(
        model="groq/compound",
        api_key=settings.groq_api_key,
        provider="groq"
)

        logger.info("✅ CrewAI Manager initialized with Groq LLM (Llama 3.1 8B)")
    
    
    def create_agents(self):
        """Create specialized AI agents"""
        
        # 1. Data Scout Agent - Finds patterns and trends
        data_scout = Agent(
            role='Data Scout',
            goal='Identify trending products, market gaps, and competitive patterns in the data',
            backstory="""You are an expert market researcher with years of experience 
            in e-commerce trend analysis. You have a keen eye for spotting emerging 
            products and understanding consumer behavior patterns.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm  # Use Gemini
        )
        
        # 2. Pricing Analyst Agent - Analyzes pricing strategies
        pricing_analyst = Agent(
            role='Pricing Strategist',
            goal='Analyze pricing patterns across platforms and recommend optimal pricing strategies',
            backstory="""You are a pricing expert who has worked with major retailers. 
            You understand competitive pricing, price elasticity, and how to maximize 
            margins while staying competitive.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm  # Use Gemini
        )
        
        # 3. Risk Assessor Agent - Identifies business risks
        risk_assessor = Agent(
            role='Risk Assessment Specialist',
            goal='Identify pricing risks, market saturation, and competitive threats',
            backstory="""You are a business risk analyst with expertise in retail markets. 
            You can identify potential problems before they become serious and suggest 
            mitigation strategies.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm  # Use Gemini
        )
        
        # 4. Demand Forecaster Agent - Predicts future demand
        demand_forecaster = Agent(
            role='Demand Forecaster',
            goal='Predict future product demand and seasonal trends',
            backstory="""You are a data scientist specializing in demand forecasting. 
            You analyze historical data, seasonality, and market signals to predict 
            future demand accurately.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm  # Use Gemini
        )
        
        # 5. Report Writer Agent - Synthesizes everything
        report_writer = Agent(
            role='Strategic Report Writer',
            goal='Synthesize all findings into actionable business recommendations',
            backstory="""You are a business consultant who creates clear, actionable 
            reports for executives. You take complex data and turn it into strategic 
            recommendations that drive business decisions.""",
            verbose=True,
            allow_delegation=True,  # Can delegate to other agents
            llm=self.llm  # Use Gemini
        )
        
        return {
            'scout': data_scout,
            'pricing': pricing_analyst,
            'risk': risk_assessor,
            'forecast': demand_forecaster,
            'writer': report_writer
        }
    
    def create_tasks(self, agents: Dict, products_data: str):
        """Create tasks for each agent"""
        
        # Task 1: Scout finds trends
        scout_task = Task(
            description=f"""Analyze the following product data and identify:
            1. Top 3 trending product categories
            2. Market gaps (underserved price points or product types)
            3. Competitive patterns (who dominates which segments)
            
            PRODUCT DATA:
            {products_data}
            
            Provide your findings in clear, bullet-point format.""",
            agent=agents['scout'],
            expected_output="A detailed analysis of trends, gaps, and competitive patterns"
        )
        
        # Task 2: Pricing analysis
        pricing_task = Task(
            description=f"""Based on this product data, analyze:
            1. Price distribution across products
            2. Which products are overpriced vs underpriced
            3. Optimal pricing strategy recommendations
            4. Price positioning vs competitors
            
            PRODUCT DATA:
            {products_data}
            
            Provide specific pricing recommendations.""",
            agent=agents['pricing'],
            expected_output="Pricing strategy with specific recommendations",
            context=[scout_task]  # Uses scout's findings
        )
        
        # Task 3: Risk assessment
        risk_task = Task(
            description=f"""Evaluate business risks in this data:
            1. Pricing risks (too high/low compared to market)
            2. Market saturation (too many similar products)
            3. Competitive threats (strong competitors)
            4. Risk mitigation strategies
            
            PRODUCT DATA:
            {products_data}
            
            Rate each risk from 1-10 and provide mitigation plans.""",
            agent=agents['risk'],
            expected_output="Risk assessment with scores and mitigation strategies",
            context=[scout_task, pricing_task]  # Uses previous findings
        )
        
        # Task 4: Demand forecasting
        forecast_task = Task(
            description=f"""Predict future demand:
            1. Which products will see increased demand
            2. Seasonal trends to watch
            3. Recommended stock levels
            4. Products likely to decline
            
            PRODUCT DATA:
            {products_data}
            
            Provide forecasts with confidence levels.""",
            agent=agents['forecast'],
            expected_output="Demand forecast with confidence levels",
            context=[scout_task]
        )
        
        # Task 5: Final report (synthesizes all)
        report_task = Task(
            description="""Create a comprehensive executive report that includes:
            1. Executive Summary (3-4 sentences)
            2. Key Findings from all analyses
            3. Top 5 Strategic Recommendations (prioritized)
            4. Action Items (what to do next)
            
            Synthesize insights from the Data Scout, Pricing Analyst, Risk Assessor, 
            and Demand Forecaster. Make it actionable for a retail manager.
            
            Format as JSON with these keys:
            {
                "executive_summary": "...",
                "key_findings": [...],
                "recommendations": [...],
                "action_items": [...]
            }""",
            agent=agents['writer'],
            expected_output="Complete JSON report with executive summary and recommendations",
            context=[scout_task, pricing_task, risk_task, forecast_task]
        )
        
        return [scout_task, pricing_task, risk_task, forecast_task, report_task]
    
    def analyze_products(self, products: List[Dict]) -> Dict:
        """
        Run the full crew analysis on product data
        
        Args:
            products: List of product dictionaries
            
        Returns:
            Comprehensive analysis report
        """
        logger.info("🚀 Starting CrewAI multi-agent analysis...")
        
        # Prepare product data summary
        products_summary = self._prepare_product_summary(products)
        
        # Create agents and tasks
        agents = self.create_agents()
        tasks = self.create_tasks(agents, products_summary)
        
        # Create the crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,  # Tasks run one after another
            verbose=True
        )
        
        # Run the crew
        try:
            logger.info("⚙️ Crew is working...")
            result = crew.kickoff()
            
            logger.info("✅ Crew analysis complete!")
            
            # Try to parse as JSON
            try:
                if isinstance(result, str):
                    # Clean potential markdown
                    clean_result = result.strip()
                    if clean_result.startswith('```json'):
                        clean_result = clean_result[7:]
                    if clean_result.startswith('```'):
                        clean_result = clean_result[3:]
                    if clean_result.endswith('```'):
                        clean_result = clean_result[:-3]
                    clean_result = clean_result.strip()
                    
                    report = json.loads(clean_result)
                else:
                    report = result
                    
            except json.JSONDecodeError:
                logger.warning("Could not parse as JSON, returning raw result")
                report = {
                    "raw_analysis": str(result),
                    "executive_summary": "Analysis completed - see raw_analysis field",
                    "key_findings": [],
                    "recommendations": [],
                    "action_items": []
                }
            
            # Add metadata
            report['total_products_analyzed'] = len(products)
            report['analysis_type'] = 'crew_ai_multi_agent'
            
            return report
            
        except Exception as e:
            logger.error(f"❌ Crew analysis failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                "error": str(e),
                "executive_summary": "Analysis failed",
                "key_findings": [],
                "recommendations": [],
                "action_items": []
            }
    
    def _prepare_product_summary(self, products: List[Dict]) -> str:
        """Convert product list to readable summary for agents"""
        summary_lines = [
            "PRODUCT CATALOG ANALYSIS",
            "=" * 60,
            f"Total Products: {len(products)}",
            ""
        ]
        
        for i, product in enumerate(products[:20], 1):  # Limit to 20 for token efficiency
            line = f"{i}. {product.get('title', 'Unknown')[:70]}"
            if product.get('price'):
                line += f" | ₹{product['price']:,.0f}"
            if product.get('rating'):
                line += f" | {product['rating']}⭐"
            if product.get('platform'):
                line += f" | [{product['platform'].upper()}]"
            summary_lines.append(line)
        
        if len(products) > 20:
            summary_lines.append(f"\n... and {len(products) - 20} more products")
        
        return "\n".join(summary_lines)

# Global instance
crew_manager = RetailIntelligenceCrew()