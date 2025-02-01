import runloop
from hub import light_matrix
from hub import port

# async def main():
#     # write your code here
#     print(port.A)
#     await light_matrix.write("Hi!")
#
# runloop.run(main())

def main():
    # write your code here
    light_matrix.write("Hi!")

runloop.run(main)


if __name__ == "__main__":
    main()