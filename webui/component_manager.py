from typing_extensions import Dict, Optional, Any, List
from typin import Component, ComponentName


UI_COMPONENTS: Dict[ComponentName, Component] = {}


def get_component(component_name : ComponentName) -> Optional[Component]:
	if component_name in UI_COMPONENTS:
		return UI_COMPONENTS[component_name]
	return None

def register_component(component_name: ComponentName, component: Component) -> bool:
    if component_name not in ComponentName.__args__:
        print(f"Component name '{component_name}' is not valid.")
        return False
    UI_COMPONENTS[component_name] = component
    return True

def update_component_value(component_name: ComponentName, new_value: Any) -> None:
    if component_name in UI_COMPONENTS:
        UI_COMPONENTS[component_name].value = new_value

