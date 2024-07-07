import os

# 定义文件夹和文件结构
project_structure = {
    "FOF_Strategy_Project": {
        "data": {
            "raw": ["fund_data.csv", "stock_data.csv", "futures_data.csv", "options_data.csv", "bonds_data.csv"],
            "processed": ["processed_fund_data.csv", "processed_stock_data.csv"]
        },
        "notebooks": ["data_exploration.ipynb", "feature_engineering.ipynb", "model_training.ipynb", "strategy_implementation.ipynb"],
        "src": {
            "__init__.py": [],
            "data": ["__init__.py", "data_loader.py", "data_cleaning.py", "data_preprocessing.py"],
            "features": ["__init__.py", "feature_extraction.py", "feature_selection.py", "feature_transformation.py"],
            "models": ["__init__.py", "regression_model.py", "rl_model.py"],
            "strategy": ["__init__.py", "strategy_implementation.py", "portfolio_management.py"],
            "backtest": ["__init__.py", "backtest.py", "evaluation.py"],
            "report": ["__init__.py", "report_generator.py"]
        },
        "tests": ["__init__.py", "test_data_loader.py", "test_feature_engineering.py", "test_model_training.py", "test_strategy_implementation.py", "test_backtest.py"],
        "requirements.txt": [],
        "README.md": [],
        "run.py": []
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        elif isinstance(content, list):
            os.makedirs(path, exist_ok=True)
            for file in content:
                open(os.path.join(path, file), 'w').close()

# 创建项目结构
create_structure('.', project_structure)
