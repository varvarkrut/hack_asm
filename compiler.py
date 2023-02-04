from hack_specifications import destination_specification
from hack_specifications import computation_specification
from hack_specifications import jump_specification
from hack_specifications import symbol_table

reg_table = {}


class FileParser:
    def __init__(self, filename):
        self.filename = filename

    def delete_whitespaces_in_file(self):
        with open(self.filename, "r") as file:
            lines = file.readlines()
        with open(self.filename, "w") as file:
            for line in lines:
                if line.strip():
                    file.write(line)

    def read_line_from_file(self):
        with open(self.filename, "r") as file:
            for line in file:
                yield line.strip("\n")

    def parse_command(self, file_line):
        if "@" in file_line:
            command_type = "a-command"
        elif "(" in file_line:
            command_type = "l-command"
        elif "=" in file_line or ";" in file_line:
            command_type = "c-command"
        else:
            command_type = "whitespace"
        return command_type, file_line


class Compiler:
    def __init__(self, filename):
        self.filename = filename
        self.symbol_table = symbol_table
        line_counter = 0
        with open(self.filename, "r") as file:
            for line in file:
                if "(" in line:
                    print(line_counter)
                    self.symbol_table[line[1:-2]] = line_counter
                line_counter += 1
        print(self.symbol_table)

    def compile_string_to_machine_code(self, command_type, hack_string):
        match command_type:
            case "whitespace":
                machine_code = ""
            case "l-command":
                machine_code = ""
            case "c-command":
                machine_code = self._compile_c_string(hack_string)

            case "a-command":
                machine_code = self._compile_a_string(hack_string)

        return machine_code

    def _compile_c_string(self, c_string):
        if "=" in c_string and ";" in c_string:
            dest = destination_specification[c_string.split("=")[0]]
            comp = computation_specification[c_string.split("=")[1]]
            jump = jump_specification[c_string.split(";")[1]]
        elif "=" in c_string:
            dest = destination_specification[c_string.split("=")[0]]
            comp = computation_specification[c_string.split("=")[1]]
            jump = jump_specification["null"]
        elif ";" in c_string:
            dest = destination_specification["null"]
            comp = computation_specification[c_string.split(";")[0]]
            jump = jump_specification[c_string.split(";")[1]]
        return f"111{comp}{dest}{jump}"

    def _compile_a_string(self, hack_string):
        if hack_string[1:].isdigit():
            return self._convert_to_15_binary(hack_string[1:])
        elif hack_string[1:] in self.symbol_table.keys():
            return self._convert_to_15_binary(self.symbol_table[hack_string[1:]])
        else:
            self.symbol_table[hack_string[1:]] = len(self.symbol_table)
            return self._convert_to_15_binary(hack_string[1:])

    def _convert_to_15_binary(self, hack_string):
        return f"0{int(hack_string):015b}"


if __name__ == "__main__":
    file_parser = FileParser("test.asm")
    compiler = Compiler("test.asm")
    for line in file_parser.read_line_from_file():
        command_type, hack_string = file_parser.parse_command(line)
        machine_code = compiler.compile_string_to_machine_code(
            command_type, hack_string
        )
        # add into file "test.hack"
        with open("test.hack", "a") as file:
            if command_type in ["a-command", "c-command"]:
                file.write(machine_code + "\n")
