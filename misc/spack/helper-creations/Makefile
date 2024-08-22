print_info: tmp_commands.txt
	pdm run python print_info.py

venv:
	pdm install

tmp_commands.txt: save_create_commands.py
	pdm run python save_create_commands.py

clean:
	rm -f tmp*
