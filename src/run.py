from streamlit.web import bootstrap

real_script = 'test_llm_simple.py'
bootstrap.run(real_script, f'run.py {real_script}', [], {})