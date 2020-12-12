import sys

PRINT_ANIKA = 0b00000001
PRINT_NUM = 0b00000010
HALT = 0b00000011
SAVE = 0b00000100
PRINT_REGISTER = 0b00000101
ADD = 0b00000110
PUSH = 0b01000111
POP = 0b01001000
CALL = 0b01001001
RET = 0b00001010

memory = [None] * 256

running = True
program_counter = 0

def load_program():
    address = 0

    # if len(sys.argv) < 2:
    #     print('Did you forget the file name?')
    #     sys.exit()

    try:
        with open(sys.argv[1], 'r') as file:
            for line in file:
                comment_split = line.split('#')

                possible_num = comment_split[0]

                if possible_num == '':
                    continue

                if possible_num[0] == '1' or possible_num[0] == '0':
                    num = possible_num[:8]
                    #print(f'{num}: {int(num, 2)}')

                    memory[address] = int(num, 2)
                    address += 1

    except FileNotFoundError:
        print(f'{sys.argv[0]}: {sys.argv[1]} not found')

load_program()

#Registers
#R0 - R7
registers = [None] * 8
registers[7] = 0xF4

while running:
    command = memory[program_counter]

    if command == PRINT_ANIKA:
        print('Anika!')
        program_counter += 1

    elif command == PRINT_NUM:
        program_counter += 1
        print(memory[program_counter])
        program_counter += 1

    elif command == SAVE:
        program_counter += 1
        number = memory[program_counter]
        program_counter += 1
        registers[memory[program_counter]] = number
        program_counter += 1

    elif command == PRINT_REGISTER:
        program_counter += 1
        index = memory[program_counter]
        print(registers[index])
        program_counter += 1

    elif command == ADD:
        program_counter += 1
        reg1 = memory[program_counter]
        program_counter += 1
        reg2 = memory[program_counter]
        registers[reg1] += registers[reg2]
        program_counter += 1

    elif command == PUSH:
        registers[7] -= 1
        program_counter += 1
        reg_idx = memory[program_counter]
        push_value = registers[reg_idx]
        sp = registers[7]
        memory[sp] = push_value
        program_counter += 1

    elif command == POP:
        sp = registers[7]
        pop_value = memory[sp]
        program_counter += 1
        reg_idx = memory[program_counter]
        registers[reg_idx] = pop_value
        registers[7] += 1
        program_counter += 1

    elif command == CALL:
        # Set up RET by grabbing the spot to return to
        next_address = program_counter + 2
        registers[7] -= 1
        sp = registers[7]
        memory[sp] = next_address
        # Go to where the function is stored
        reg_address = memory[program_counter + 1]
        jump_to = registers[reg_address]
        program_counter = jump_to

    elif command == RET:
        sp = registers[7]
        return_address = memory[sp]
        registers[7] += 1
        program_counter = return_address

    elif command == HALT:
        running = False

    else:
        print('Command not recognized!')
        break
