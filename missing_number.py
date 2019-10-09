import argparse,os

def missingNumber(nums):
    missing = len(nums)
    for i, num in enumerate(nums):
        missing ^= i ^ num
    return missing

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    nums=[]
    if os.path.isfile(args.filename):
		nums  = [line.rstrip('\n') for line in open(args.filename)]
    else:
		print(" Path of File {} doesnot exist".format(args.filename))
    nums = list(map(int, nums))
    print(missingNumber(nums))
if __name__=='__main__':
        main()


"""
Answer the following questions in addition to your functional code
- What’s the runtime and space complexity of your solution?
Time Complexity:  O(n)
Assuming that XOR is a constant-time operation, this algorithm does constant work on n iterations, so the runtime is overall linear
Space Complexity: O(n)
As we read the elements from file to a list
- How can you optimize your solution further?
  Don’t read the elements from file to list instead just compute xor and return the missing number for
  O(1)  space
- What test cases you’d write against your function?
1>      Empty file
2>      Non-Integers
3>      Duplicate numbers

"""
