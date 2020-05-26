import os

schemes = dict()
schemes['rnd'] = 'r'
schemes['iolts'] = 'i'

# schemes['toc13mux'] = 't'
# schemes['toc13xor'] = 't'

benches = ['apex2','apex4','c432','c499','c880','c1355','c1908','c2670','c3540','c5315','c7552','dalu','des','ex5','ex1010','i4','i7','i8','i9','k2','seq']
for scheme in schemes.keys():
    for bench in benches:
        for f in range(20, 21):
            command = ''
            if scheme == 'toc13xor':
                command = './source/src/sle -t -f ' + str(f*0.01) + ' -o ../../transfer/host15-logic-encryption/benchmarks/'+scheme+'/'+bench+'_enc'+str(f)+'.bench '+'./benchmarks/original/'+bench+'.bench'
                # print(command)
            elif scheme == 'toc13mux':
                command = './source/src/sle -t -f ' + str(f*0.01) + ' -s -o ../../transfer/host15-logic-encryption/benchmarks/'+scheme+'/'+bench+'_enc'+str(f)+'.bench '+'./benchmarks/original/'+bench+'.bench'
            else:
                command = './source/src/sle -'+schemes[scheme]+' -f ' + str(f*0.01) + ' -o ../../transfer/host15-logic-encryption/benchmarks/'+scheme+'/'+bench+'_enc'+str(f)+'.bench '+'./benchmarks/original/'+bench+'.bench'
            os.popen(command)

