import os
import random

base_dir = '/home/tanqinhan/Desktop/CamouflagedLogic/tmp/host15-logic-encryption'
sld = base_dir + '/bin/sld '
lcmp = base_dir + '/bin/lcmp '
benches = ['apex2', 'apex4', 'c432', 'c499', 'c880', 'c1355', 'c1908', 'c2670', 'c3540', 'c5315', 'c7552', 'dalu', 'des', 'ex5', 'ex1010', 'i4', 'i7', 'i8', 'i9', 'k2', 'seq', 'vscale_core']
# benches = ['vscale_core']
dirs = [bench + '_enc05' for bench in benches]  # All the benches to be tested
results = []

# for bench in benches:
# results = []
percentage = 1
os.popen('mkdir -p ' + base_dir + '/benchmarks/mux/' + str(percentage) + 'percent/')
for dir in dirs:
    repeat = 100
    total_time = 0
    min = -1
    max = -1
    bench = dir[:dir.find('_enc')]
    for i in range(0, repeat):
        file = open(base_dir + '/benchmarks/rnd/' + dir + '.bench')
        content = file.readlines()
        file.close()
        inputs = []
        key_num = 0
        mark = 0
        for index in range(0, len(content)):
            line = content[index]
            if line.find('OUTPUT') >= 0 and len(inputs) == 0:
                inputs = content[: index]
                key_num = int(inputs[-1][inputs[-1].find('keyinput') + 8: inputs[-1].find(')')])
                mark = index
                # print(key_num)
            if line.find('=') >= 0:
                if random.randint(1, 100) > percentage:
                    continue
                gate = line[: line.find(' = ')]
                terms = line[line.find('(') + 1: line.find(')')].split(', ')

                if line.find('nand') >= 0 or line.find('nor') >= 0 or line.find('xor') >= 0:
                    if len(terms) == 2:
                        inputs.append('INPUT(keyinput' + str(key_num + 1) + ')\n')
                        inputs.append('INPUT(keyinput' + str(key_num + 2) + ')\n')
                        new_line = 'keyinput' + str(key_num + 1) + '_not = not(keyinput' + str(key_num + 1) + ')\n'
                        new_line += 'keyinput' + str(key_num + 2) + '_not = not(keyinput' + str(key_num + 2) + ')\n'
                        new_line += gate + '_nand = nand(' + ', '.join(terms) + ')\n'
                        new_line += gate + '_nand_o = and(' + gate + '_nand, ' + 'keyinput' + str(
                            key_num + 1) + ', keyinput' + str(key_num + 2) + ')\n'
                        new_line += gate + '_nor = nor(' + ', '.join(terms) + ')\n'
                        new_line += gate + '_nor_o = and(' + gate + '_nor, ' + 'keyinput' + str(
                            key_num + 1) + '_not' + ', keyinput' + str(key_num + 2) + ')\n'
                        new_line += gate + '_xor = xor(' + ', '.join(terms) + ')\n'
                        new_line += gate + '_xor_o = and(' + gate + '_xor, ' + 'keyinput' + str(
                            key_num + 1) + ', keyinput' + str(key_num + 2) + '_not' + ')\n'
                        new_line += gate + '_xnor = xnor(' + ', '.join(terms) + ')\n'
                        new_line += gate + '_xnor_o = and(' + gate + '_xnor, ' + 'keyinput' + str(
                            key_num + 1) + '_not' + ', keyinput' + str(key_num + 2) + '_not' + ')\n'
                        new_line += gate + ' = or(' + gate + '_nand_o, ' + gate + '_nor_o, ' + gate + '_xor_o, ' + gate + '_xnor_o)\n'
                        key_num += 3
                        content[index] = new_line
                    elif len(terms) > 2:
                        inputs.append('INPUT(keyinput' + str(key_num + 1) + ')\n')
                        new_line = 'keyinput' + str(key_num + 1) + '_not = not(keyinput' + str(key_num + 1) + ')\n'
                        new_line += gate + '_nand = nand(' + ', '.join(terms) + ')\n'
                        new_line += gate + '_nand_o = and(' + gate + '_nand, ' + 'keyinput' + str(
                            key_num + 1) + ')\n'
                        new_line += gate + '_nor = nor(' + ', '.join(terms) + ')\n'
                        new_line += gate + '_nor_o = and(' + gate + '_nor, ' + 'keyinput' + str(
                            key_num + 1) + '_not' + ')\n'
                        new_line += gate + ' = or(' + gate + '_nand_o, ' + gate + '_nor_o)\n'
                        key_num += 2
                        content[index] = new_line
                elif line.find(' and(') >= 0 or line.find(' or(') >= 0:
                    inputs.append('INPUT(keyinput' + str(key_num + 1) + ')\n')
                    new_line = 'keyinput' + str(key_num + 1) + '_not = not(keyinput' + str(key_num + 1) + ')\n'
                    new_line += gate + '_and = and(' + ', '.join(terms) + ')\n'
                    new_line += gate + '_and_o = and(' + gate + '_and, ' + 'keyinput' + str(
                        key_num + 1) + ')\n'
                    new_line += gate + '_or = or(' + ', '.join(terms) + ')\n'
                    new_line += gate + '_or_o = and(' + gate + '_or, ' + 'keyinput' + str(
                        key_num + 1) + '_not' + ')\n'
                    new_line += gate + ' = or(' + gate + '_and_o, ' + gate + '_or_o)\n'
                    key_num += 2
                    content[index] = new_line
        content = inputs + content[mark:]
        file = open(base_dir + '/benchmarks/mux/' + str(percentage) + 'percent/' + dir + '.bench', 'w')
        file.write(''.join(content))
        file.close()
        #

        command = sld + base_dir + '/benchmarks/mux/' + str(percentage) + 'percent/' + dir + '.bench ' + base_dir + '/benchmarks/original/' + bench + '.bench'
        # print(command)
        output = os.popen(command).read().strip('\n')
            # print(output)
        info = output[output.find('key='): output.find('iteration=') - 1]
        time = float(output[output.find('cpu_time') + 9: output.find('maxrss') - 2])
        total_time += time
        if time > max or max == -1:
            max = time
        if time < min or min == -1:
            min = time

        if output.find('key=x') >= 0:
            results.append(bench + ' UNSAT')
            break
        else:
            key = output[output.find('key=') + 4: output.find('iteration=')].replace('\n', '')
            result = os.popen(
                lcmp + base_dir + '/benchmarks/original/' + bench + '.bench ' + base_dir + '/benchmarks/mux/' + str(percentage) + 'percent/' + dir + '.bench key=' + key).read()
            if result.find('different') >= 0:
                results.append(bench + ' different')
                break
            # elif result.find('equivalent') >= 0:
            #     print('equivalent')
    results.append(bench + ' ' + str(total_time / repeat) + ' ' + str(min) + ' ' + str(max))
    file = open(base_dir + '/benchmarks/mux/' + str(percentage) + 'percent/result.txt', 'w')
    file.write('\n'.join(results))
    file.close()


