import google.generativeai as genai
import asyncio
from typing import Dict, Any, Awaitable, Callable, List
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from backend.utils.config import get_settings

from backend.agents.personalities.jordan import JordanAgent, test_jordan 
from backend.agents.personalities.maya import MayaAgent, test_maya 
from backend.agents.personalities.river import RiverAgent, test_river 
from backend.agents.personalities.sam import SamAgent, test_sam
from backend.agents.personalities.alex import AlexAgent, test_alex
from backend.agents.personalities.dr_chen import DrChenAgent, test_dr_chen                                                                                                                                                                          

async def run_all_agent_tests(test_functions: List[Callable[[], Awaitable[None]]]) -> None:
    """
    Runs a list of asynchronous test functions sequentially and logs their execution.
    
    Args:
        test_functions (List[Callable]): A list of the async test functions to execute.
    """
    print("=" * 70)
    print("STARTING UNIFIED AGENT TEST RUNNER")
    print("=" * 70)
    
    try:
        settings = get_settings()
        genai.configure(api_key=settings.google_api_key)
        print("GenAI configuration initialized.")
    except Exception as e:
        print(f"Configuration Error: Could not load settings or configure GenAI. {e}")
        return

    for test_func in test_functions:
        agent_name = test_func.__name__.replace('test_', '').upper()
        print(f"\n--- Running Test for {agent_name} Agent ---")
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            await test_func()
            end_time = asyncio.get_event_loop().time()
            duration = end_time - start_time
            print(f"{agent_name} Test Completed successfully in {duration:.2f} seconds.")
        except Exception as e:
            print(f"{agent_name} Test FAILED: {e}")
            
    print("\n" + "=" * 70)
    print("ALL AGENT TESTS FINISHED")
    print("=" * 70)

if __name__ == "__main__":
    all_tests = [
        test_jordan,
        test_maya,
        test_river,
        test_sam,
        test_alex,
        test_dr_chen
    ]
    
    asyncio.run(run_all_agent_tests(all_tests))