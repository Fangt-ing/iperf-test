import sys
import importlib.util

class ScriptCaller:
    def __init__(self, script_names):
        self.script_names = script_names

    def call_scripts(self):
        for script_name in self.script_names:
            try:
                # Load the script dynamically
                spec = importlib.util.spec_from_file_location("module.name", script_name)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Execute the main function of the script
                if hasattr(module, 'main'):
                    print(f"Calling script: {script_name}")
                    module.main()
                else:
                    print(f"No 'main' function found in script: {script_name}")

            except FileNotFoundError:
                print(f"Script not found: {script_name}")
            except Exception as e:
                print(f"Error calling script {script_name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python caller.py script1.py script2.py ...")
        sys.exit(1)

    script_names = sys.argv[1:]
    script_caller = ScriptCaller(script_names)
    script_caller.call_scripts()
