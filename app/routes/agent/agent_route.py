from flask import Blueprint
from .agent_controller import AgentController

agent_bp = Blueprint('agent', __name__)

agent_controller = AgentController()


@agent_bp.route('/generate-text', methods=['POST'])
def generate_text():
    return agent_controller.generate_text_controller()