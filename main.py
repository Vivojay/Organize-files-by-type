from tabulate import tabulate as tbl
import sys
import os
import shutil
import subprocess as sp

#Works from DOS

def INIT():
    with open(os.path.join(os.path.split(__file__)[0], '._orig.obb')) as f:
        a = f.read()

    with open(os.path.join(os.path.split(__file__)[0], 'blacklist.bb')) as f:
        # print(f.read())
        if f.read().isspace() or f.read() == '':
            with open(os.path.join(os.path.split(__file__)[0], 'blacklist.bb'), 'w') as f:
                f.write(a)
                print('Blacklist was reset')

'''
try:
    with open(os.path.join(os.path.split(__file__)[0], '._orig.obb')) as f:
        a=f.read()
        print('py ' + '"' + __file__ + '" -b '+a, shell = True)
        # sp.Popen('py ' + '"' + __file__ + '" -b '+a, shell = True)
except:
    print('Error Running Script, exiting . . .')
    os._exit(0)
'''

# Default blacklisted files stored in file: ._orig.obb

args = sys.argv[1:]
openDir = False #Default Value

if args == []:
    print('No args entered, exiting . . .')
    os._exit(0)

# print('arg(s) =', args)

mainDir = os.path.split(__file__)[0]
os.chdir(mainDir)

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))


if not os.path.exists(os.path.join(mainDir, 'blacklist.bb')):
    with open('blacklist.bb', 'a', encoding = 'utf-8-sig') as f:
        print('Created an empty blacklist')
        INIT()

if (set([os.path.isdir(i) for i in args if not i in ['-ob', '-o', '-h']]) == {True}):
    isDir = True
else:
    isDir = False


if ' '.join(args).startswith('-b '):
    exts = ([i[1:] if i.startswith('.') else i for i in args[1:]])

    with open('blacklist.bb', 'r', encoding = 'utf-8-sig') as f:
        alreadyAdded = set([i for i in list(set(f.read().split('\n'))) if not i == ''])
    blackList = set([i for i in (set(exts)) if not i == ''])

    if (blackList - alreadyAdded != set()):
        with open('blacklist.bb', 'a', encoding = 'utf-8-sig') as f:
            f.write('\n'+'\n'.join(blackList - alreadyAdded))
    print('added', len(blackList - alreadyAdded), 'new extensions')


elif ' '.join(args).strip() == '-bc':
    with open('blacklist.bb', 'w', encoding = 'utf-8-sig') as f:
        f.write('')
    print('cleared all extensions')


elif ' '.join(args).strip() == '-br':
    with open('blacklist.bb', 'r', encoding = 'utf-8-sig') as f:
        a = ([i for i in f.read().split() if not i == '' or i.isspace()])

    print()
    print(tbl(list(chunks(a, 4)), tablefmt = 'plain'))
    print()

elif '-h' in args:
    with open('help.txt') as f:
        print(f.read())

if isDir:
    files = []

    if not '-ob' in args:
        with open('blacklist.bb', 'r', encoding = 'utf-8-sig') as f:
            alreadyAdded = [i for i in list(set(f.read().split('\n'))) if not i == '']
            # print('>>>', alreadyAdded)
    else:
        alreadyAdded = []
    
    if '-o' in args:
        openDir = True

    for i in ['-ob', '-o']:
        try:
            args.remove(i)
        except Exception:
            pass

    for i in args:
        temp = []
        for j in os.listdir(i):
            if os.path.splitext(j)[1][1:] not in alreadyAdded:
                temp.append(os.path.join(i, j))
                # print(os.path.join(i, j))
        files.append(temp)


    # print(files)

    flat_list = [item for sublist in files for item in sublist]
    exts = [os.path.splitext(i)[1] for i in flat_list]
    exts = set(exts)

    if '' in set(exts):
        exts.remove('')

    # print()
    # print(flat_list)
    # print()
    # print(exts)

    for f in files:
        # print('-'*80)
        # print('-'*80)
        # print()
        for k in [[i for i in f if i.endswith(x)] for x in exts]:
            if k != []:
                # print(k)
                print(os.path.splitext(k[0])[1][1:])
                os.chdir(os.path.split(k[0])[0])

                try:
                    os.mkdir(os.path.splitext(k[0])[1][1:]+'_files')
                except FileExistsError:
                    pass
 
                for file in k:
                    print('\t>', file)
                    # print(file, ', ', os.path.splitext(k[0])[1][1:]+'_files', sep = '')
                    try:
                        shutil.move(file, os.path.splitext(k[0])[1][1:]+'_files')
                    except:
                        print("\t\tCouldn't move \"", os.path.split(file)[1], '\" to ', '"'+os.path.splitext(k[0])[1][1:]+'_files"', sep = '')

# print(args[0], openDir)

if openDir:
    sp.Popen('explorer /select,"'+ args[0] +'"')
