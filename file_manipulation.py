import re

# file loading from existing file
def gen_list_from(filename):
    id_list_to_follow = []
    with open(filename,'r') as f:#フォロー対象のリストの読み込み
        for line in f:
            id_list_to_follow.append(line.strip())
    return id_list_to_follow

def read_txt_from(filename):
  txt = ''
  with open(filename, 'r') as f:
    txt = f.read()
  return txt

# saving of file
def create_new_file(filename):
  with open(filename, 'w') as f:
    f.write('')

def overwrite(filename, txt):
  with open(filename, 'w') as f:
    f.write(txt)

# manipulation of existing file
def pop_from(filename): # pop a line from file without \n
  txt = read_txt_from(filename)
  id_list = txt.split('\n')
  try:
    id_popped = id_list.pop(0)
    overwrite(filename, '\n'.join(id_list))
    print('{} popped from {}'.format(id_popped, filename))
    return id_popped
  except:
    print('pop_from {} failed ... ToT'.format(filename))

def add_line_with_n(filename,string):
  with open(filename, 'a') as f:
    f.write(string + '\n')

def trim_file(filename):
  with open(filename, 'r') as f_input:
    txt = f_input.read()
  with open(filename, 'w') as f_input:
    f_input.write(txt.replace('/', ''))
