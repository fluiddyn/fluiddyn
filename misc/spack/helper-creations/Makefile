
develop:
	pdm install

tmp_commands.txt: save_create_commands.py
	pdm run python save_create_commands.py

get_info: tmp_commands.txt
	pdm run python get_info.py

clean:
	rm -f tmp*
