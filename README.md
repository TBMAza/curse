# curse
Small AI tool to control your cursor with voice commands

# Run
1. `git clone https://github.com/TBMAza/curse.git`
2. `cd curse`
3. `python -m venv .venv`
4. `pip install -r requirements.txt`
5. `source .venv/bin/activate`
6. Download a model in .gguf format and assign its path to global variable LLM_MODEL at line 10 in curse.py
7. `python curse.py`
8. Speak in natural language and tell your cursor what to do

# Currently available cursor actions
- Move in any direction horizontally, vertically, and diagonally. Give exact number of pixels to move across or simply tell to move slightly, all the way, etc. in any direction, just how you would with a human colleague;
- Right click, left click, double click.

# Change language
Change line 24:
```python
stt_model = Model(lang="it") # currently set to Italian; change to whatever you need
```
