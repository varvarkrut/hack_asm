import re
from hack_specifications import destination_specification
from hack_specifications import computation_specification
from hack_specifications import jump_specification
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
                yield line.strip('\n')

    def parse_command(self, file_line):
        if "@" in line:
            pass
        else:
            parsed_c_string = re.split(
                "=|;", file_line.replace(" ", "")
            )  # dest = comp ; jump
            dest = parsed_c_string[0]
            comp = parsed_c_string[1]
            try:
                jump = parsed_c_string[2]
            except IndexError:
                jump = "null"
            command_type = "c-command"
            c_string = f"{dest};{comp};{jump}"
            return command_type, c_string


class Compiler:

    def compile_string_to_machine_code(self, command_type, hack_string):
        match command_type:
            case "c-command":
                machine_code = self._compile_c_string(hack_string)

            case "a-command":
                machine_code = self._compile_a_string(hack_string)

        return machine_code

    def _compile_c_string(self, c_string):

        dest_in_binary = destination_specification[c_string.split(";")[0]]
        comp_in_binary = computation_specification[c_string.split(";")[1]]
        try:
            jump_in_binary = jump_specification[c_string.split(";")[2]]
        except KeyError:
            jump_in_binary = "000"

        return f"111{comp_in_binary}{dest_in_binary}{jump_in_binary}"

    def _compile_a_string(self, hack_string):
        return hack_string


if __name__ == "__main__":
    file_parser = FileParser("test.asm")
    file_parser.delete_whitespaces_in_file()
    compiler = Compiler()
    for line in file_parser.read_line_from_file():
        command_type, hack_string = file_parser.parse_command(line)
        machine_code = compiler.compile_string_to_machine_code(
            command_type, hack_string
        )
        print(machine_code)