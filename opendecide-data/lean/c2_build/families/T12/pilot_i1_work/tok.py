import sys
sys.path.insert(0, '.')
sys.dont_write_bytecode = True
from c2_kit import cards
mx, tok = cards._tokenizer()
def n(s): return len(tok.encode(s, add_special_tokens=False).ids)
if __name__ == '__main__':
    for line in sys.stdin.read().split('\n'):
        print(n(line), '|', line)
