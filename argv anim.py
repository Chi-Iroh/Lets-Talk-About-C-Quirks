from manimlib import *

class ArgvAnimation(Scene):
    def construct(self):
        # Words inside the array
        words = ["./a.out", "hello", "world", "NULL"]

        INSTRUCTIONS_LEFTMOST_X = 5 * LEFT
        LEFTMOST_ARRAY_X = 1 * LEFT
        BOTTOMMOST_Y = 3 * DOWN

        command_text = Text(
            "./a.out hello world"
        ).move_to(BOTTOMMOST_Y).set_color(ORANGE).set_color_by_text("./a.out", GREEN)
        self.play(ShowCreation(command_text))

        # Create boxes for array elements
        array = VGroup(*[
            Square(side_length=1.75).set_color(GREEN if i == 0 else BLUE if i == len(words) - 1 else WHITE).move_to(LEFTMOST_ARRAY_X + i * RIGHT * 2)
            for i in range(len(words))
        ])

        # Create text labels inside boxes
        text_labels = VGroup(*[
            Text(word).scale(0.8).move_to(square).set_color(BLUE if word == "NULL" else GREEN if word == "./a.out" else WHITE) for word, square in zip(words, array)
        ])

        instructions = VGroup(*[
            Text(f"puts(\"{argv}\")").scale(0.8).set_color_by_text(f"\"{argv}\"", ORANGE).move_to(INSTRUCTIONS_LEFTMOST_X)
            for argv in words
        ])
        argv_increment_text = Text("argv++").move_to(INSTRUCTIONS_LEFTMOST_X)
        return_increment_text = Text("return").move_to(INSTRUCTIONS_LEFTMOST_X).set_color(BLUE)
        instruction = None

        # Create pointer arrow
        pointer = Arrow(UP, DOWN, buff=0.3).set_color(RED)
        pointer.next_to(array[0], UP)  # Start pointing to first cell
        argv_label = Text("argv").scale(0.8).next_to(pointer, UP).set_color(ORANGE)

        self.play(ShowCreation(array), FadeIn(text_labels))
        self.play(ShowCreation(pointer), FadeIn(argv_label))
        self.wait(1)

        n_argv = len(array)
        for i in range(n_argv):
            is_last_elem = i == n_argv - 1
            if i == 0:
                instruction = instructions[0]
                self.play(ShowCreation(instruction))
            elif is_last_elem:
                self.play(Transform(instruction, return_increment_text))
            else:
                self.play(Transform(instruction, instructions[i]))
            self.wait(1)
            if not is_last_elem:
                self.play(Transform(instruction, argv_increment_text))

            if not is_last_elem:
                self.play(
                    ApplyMethod(pointer.next_to, array[i + 1], UP),
                    run_time=0.5
                )
                self.play(
                    ApplyMethod(argv_label.next_to, pointer, UP),
                    run_time=0.5
                )
            self.wait(1)
