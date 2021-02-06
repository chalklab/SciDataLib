from SciDataLib.SciData import *

example = SciData('test')

# example.author([{'name':'Dylan'}])
# example.author(['Dylan'])


print(json.dumps(example.output, indent=4, ensure_ascii=False))
