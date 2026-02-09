from crewai import Agent, Task, Crew, Process
from typing import List, Dict
import json
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RetailIntelligenceCrew:
    """Multi-agent system for comprehensive retail analysis"""

    def create_agents(self) -> Dict[str, Agent]:
        """Create specialized AI agents using Groq"""

        MODEL = "groq/compound-mini"

        data_scout = Agent(
            role="Data Scout",
            goal="Identify trending products, market gaps, and competitive patterns",
            backstory=(
                "You are an expert market researcher with deep experience in "
                "e-commerce trends, consumer behavior, and competitive analysis."
            ),
            llm=MODEL,
            verbose=True,
            allow_delegation=False,
        )

        pricing_analyst = Agent(
            role="Pricing Strategist",
            goal="Analyze pricing patterns and recommend optimal pricing strategies",
            backstory=(
                "You are a pricing expert who understands margins, elasticity, "
                "and competitive positioning in retail markets."
            ),
            llm=MODEL,
            verbose=True,
            allow_delegation=False,
        )

        risk_assessor = Agent(
            role="Risk Assessment Specialist",
            goal="Identify market, pricing, and competitive risks",
            backstory=(
                "You are a retail risk analyst skilled at identifying saturation, "
                "pricing wars, and structural weaknesses before they escalate."
            ),
            llm=MODEL,
            verbose=True,
            allow_delegation=False,
        )

        demand_forecaster = Agent(
            role="Demand Forecaster",
            goal="Forecast short-term and medium-term product demand",
            backstory=(
                "You are a data-driven forecaster who analyzes seasonality, "
                "market signals, and historical behavior to predict demand."
            ),
            llm=MODEL,
            verbose=True,
            allow_delegation=False,
        )

        report_writer = Agent(
            role="Strategic Report Writer",
            goal="Synthesize insights into clear, actionable business recommendations",
            backstory=(
                "You are a consultant who converts complex analysis into "
                "executive-ready insights and action plans."
            ),
            llm=MODEL,
            verbose=True,
            allow_delegation=True,
        )

        return {
            "scout": data_scout,
            "pricing": pricing_analyst,
            "risk": risk_assessor,
            "forecast": demand_forecaster,
            "writer": report_writer,
        }

    def create_tasks(
        self, agents: Dict[str, Agent], products_data: str
    ) -> List[Task]:
        """Create tasks for each agent"""

        scout_task = Task(
            description=f"""
Analyze the product data and identify:
- Emerging product categories
- Common traits of high-performing products
- Market gaps or opportunities

PRODUCT DATA:
{products_data}
""",
            agent=agents["scout"],
            expected_output="Market trends and opportunity analysis",
        )

        pricing_task = Task(
            description=f"""
Analyze pricing across products:
- Identify overpriced and underpriced items
- Recommend pricing adjustments
- Explain rationale clearly

PRODUCT DATA:
{products_data}
""",
            agent=agents["pricing"],
            expected_output="Pricing recommendations with justification",
        )

        risk_task = Task(
            description=f"""
Identify risks in the current product portfolio:
- Market saturation
- Competitive threats
- Pricing pressure
- Inventory or positioning risks

PRODUCT DATA:
{products_data}
""",
            agent=agents["risk"],
            expected_output="Prioritized risks with mitigation strategies",
        )

        forecast_task = Task(
            description=f"""
Forecast demand for key products:
- 1-month and 3-month outlook
- Seasonality considerations
- Products likely to spike or decline

PRODUCT DATA:
{products_data}
""",
            agent=agents["forecast"],
            expected_output="Demand forecasts with confidence levels",
        )

        writer_task = Task(
            description="""
Synthesize all agent outputs into an executive report:
- Key insights
- Top 5 recommendations
- 30 / 90 day action plan
""",
            agent=agents["writer"],
            expected_output="Executive-ready strategic report",
        )

        return [
            scout_task,
            pricing_task,
            risk_task,
            forecast_task,
            writer_task,
        ]

    def analyze_products(self, products: List[Dict]) -> Dict:
        """Run the multi-agent analysis"""

        logger.info("⚙️ Preparing crew and tasks...")

        products_summary = self._prepare_product_summary(products)

        agents = self.create_agents()
        tasks = self.create_tasks(agents, products_summary)

        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )

        try:
            logger.info("🚀 Crew execution started...")
            result = crew.kickoff()
            logger.info("✅ Crew execution completed")

            if isinstance(result, str):
                try:
                    return json.loads(result)
                except Exception:
                    return {"result": result}

            return result

        except Exception as e:
            logger.error(f"❌ Crew execution failed: {e}")
            return {"error": str(e)}

    def _prepare_product_summary(self, products: List[Dict]) -> str:
        """Condense product data for LLM context"""

        lines = []
        for i, product in enumerate(products[:20]):
            line = f"{i+1}. {product.get('title', 'Untitled')}"
            if product.get("price"):
                line += f" | ₹{product['price']}"
            if product.get("rating"):
                line += f" | {product['rating']}⭐"
            if product.get("platform"):
                line += f" | [{product['platform'].upper()}]"
            lines.append(line)

        if len(products) > 20:
            lines.append(f"... and {len(products) - 20} more products")

        return "\n".join(lines)


# Global instance
crew_manager = RetailIntelligenceCrew()
