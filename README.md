# KanaEx
An application to exercise hiragana and katakana. You can see your progress everytime you call the program.

## Usage
First, you'll need a profile to save your progress. You can give your profile name while you're calling the program as shown below:
```console
foo@bar:~$ python3 kanaex.py foo

Created player foo
```
Another option is; you'll be prompted for a profile name automatically if there isn't any profile (a ```yaml``` file with profile name) exists.
```console
foo@bar:~$ python3 kanaex.py
Enter a name to start:
foo
```

After your profile is created program will asks you to choose a game mode. There is only hiragana, katakana and mixed game modes for now.

Have Fun!

### TODO
1. Add docstrings
2. Align elements properly
