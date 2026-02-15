from crewai import Agent, Task, Crew, Process
from typing import List, Dict
import json
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RetailIntelligenceCrew:
    """Multi-agent system for comprehensive retail analysis"""

    def __init__(self, task_delay_seconds: int = 15):
        """
        Initialize the crew manager.

        Args:
            task_delay_seconds: Delay in seconds between task executions to avoid rate limits (default: 15)
        """
        self.task_delay_seconds = task_delay_seconds
        logger.info(
            f"⏱️ Task delay set to {task_delay_seconds} seconds between executions"
        )

    def create_agents(self) -> Dict[str, Agent]:
        """Create specialized AI agents using Groq"""

        MODEL = "groq/llama-3.1-8b-instant"

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

    def create_tasks(self, agents: Dict[str, Agent], products_data: str) -> List[Task]:
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
        """Run the multi-agent analysis with rate limiting"""

        logger.info("⚙️ Preparing crew and tasks...")

        products_summary = self._prepare_product_summary(products)

        agents = self.create_agents()
        tasks = self.create_tasks(agents, products_summary)

        # Execute tasks sequentially with delays
        try:
            logger.info("🚀 Sequential execution with rate limiting started...")
            results = []

            for i, task in enumerate(tasks, 1):
                logger.info(f"📋 Executing Task {i}/{len(tasks)}: {task.agent.role}")

                # Create a mini-crew for this single task
                mini_crew = Crew(
                    agents=[task.agent],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=True,
                )

                task_result = mini_crew.kickoff()
                results.append({"agent": task.agent.role, "output": str(task_result)})

                logger.info(f"✅ Task {i} completed")

                # Add delay between tasks (except after the last one)
                if i < len(tasks):
                    logger.info(
                        f"⏳ Waiting {self.task_delay_seconds} seconds before next task..."
                    )
                    time.sleep(self.task_delay_seconds)

            # Final report is the last task's output
            final_report = results[-1]["output"] if results else "No results generated"

            logger.info("✅ All tasks completed successfully")

            return {
                "final_report": final_report,
                "detailed_results": results,
                "tasks_completed": len(results),
            }

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
# Adjust task_delay_seconds here to change the delay between all task executions
# Examples:
#   - crew_manager = RetailIntelligenceCrew(task_delay_seconds=15)  # 15 seconds (default)
#   - crew_manager = RetailIntelligenceCrew(task_delay_seconds=30)  # 30 seconds
#   - crew_manager = RetailIntelligenceCrew(task_delay_seconds=60)  # 60 seconds (1 minute)
crew_manager = RetailIntelligenceCrew(task_delay_seconds=60)
