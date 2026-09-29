from flask import Blueprint

from .vision_controller import VisionController


vision_bp = Blueprint(
    "vision",
    __name__,
    url_prefix="/api/vision"
)

vision_controller = VisionController()


@vision_bp.route("/analyze", methods=["POST"])
def analyze_image_route():
    return vision_controller.analyze_image_controller()