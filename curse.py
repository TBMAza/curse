import json
import queue
import sounddevice as sd
import pyautogui as ag
from vosk import Model, KaldiRecognizer
from llama_cpp import Llama

SR = 16_000
BLKSZ = 8_000
LLM_MODEL = "./qwen-q2.gguf"
VALID_ACTIONS = ["exit", "dclick", "lclick", "rclick", "move"]
JSON_SCHEMA = {
	"type": "object",
	"properties": {
		"action": {"type": "string", "enum": ["exit", "dclick", "lclick", "rclick", "move"]},
		"x": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
		"y": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
	},
	"required": ["action", "x", "y"],
	"additionalProperties": False,
}

q = queue.Queue()
stt_model = Model(lang="it")
rec = KaldiRecognizer(stt_model, SR)
llm = Llama(model_path=LLM_MODEL, n_ctx=2048, n_gpu_layers=-1, verbose=False,)

def callback(indata, frames, time, status):
	q.put(bytes(indata))

with sd.RawInputStream(samplerate=SR, blocksize=BLKSZ, dtype="int16", channels=1, callback=callback):
	while True:
		print("listening...")

		data = q.get()
		command = None
		if rec.AcceptWaveform(data):
			command = json.loads(rec.Result())["text"]
		response = None
		if command:
			print(f"command: {command}")
			
			with open("./sysprompt.txt", "r") as f:
				sysprompt = f.read()
			w, h = ag.size()
			sysprompt = sysprompt.replace("[DISPLAY_SIZE]", f"{w}x{h}")
			
			response = llm.create_chat_completion(
				messages=[
					{"role": "system", "content": sysprompt},
					{"role": "user", "content": command}
				],
				response_format={"type": "json_object", "schema": JSON_SCHEMA},
				max_tokens=100,
				temperature=0,
			)["choices"][0]["message"]["content"]
			print(f"response: {response}")

			try:
				instruction = json.loads(response)
			except Exception:
				continue

			action = instruction.get("action")
			if action not in VALID_ACTIONS:
				continue
			
			if action == "exit":
				print("action: exit")
				break
			elif action == "dclick":
				print("action: double click")
				ag.doubleClick()
			elif action == "lclick":
				print("action: left click")
				ag.click()
			elif action == "rclick":
				print("action: right click")
				ag.rightClick()
			elif action == "move":
				try:
					x = int(float(instruction.get("x")))
					y = int(float(instruction.get("y")))
				except Exception:
					continue
				print(f"action: move towards ({x}, {y})")
				ag.move(x, y, duration=.25)
			else:
				continue
# EOF
