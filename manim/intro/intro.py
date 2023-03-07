from manim import *

class intro(Scene):
    def construct(self):
        Box = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        text = Text("Car")
        Block = VGroup(Box, text)
        self.play(FadeIn(Block))
        self.wait(0.5)

        BlockInputText = Text("Throttle").scale(0.8)
        BlockInputText.add_updater(lambda m: m.next_to(Box, 4 * LEFT))
        BlockInputArrow = Arrow(BlockInputText.get_right(), BlockInputText.get_right() + RIGHT)
        BlockInputArrow.add_updater(lambda m: m.next_to(BlockInputText, RIGHT))
        
        airInputText = Text("air").scale(0.5)
        fuelInputText = Text("fuel").scale(0.5)
        airandfuel = VGroup(airInputText, fuelInputText).arrange(3 * RIGHT)
        airandfuel.add_updater(lambda m: m.next_to(Block, DOWN * 4))
        airInputArrow = Arrow(airInputText.get_top(), airInputText.get_top() + UP)     
        airInputArrow.add_updater(lambda m: m.next_to(airandfuel[0], UP))
        fuelInputArrow = Arrow(fuelInputText.get_top(), fuelInputText.get_top() + UP)
        fuelInputArrow.add_updater(lambda m: m.next_to(airandfuel[1], UP))
        
        self.play(FadeIn(BlockInputText),
                  FadeIn(BlockInputArrow))
        
        self.play(Circumscribe(Block, buff = 0),
                  FadeIn(airandfuel),
                  FadeIn(fuelInputArrow),
                  FadeIn(airInputArrow),
                  )

        BlockOutputText = Text("Motion").scale(0.8)
        BlockOutputText.add_updater(lambda m: m.next_to(Box, 4 * RIGHT))
        BlockOutputArrow = Arrow(BlockOutputText.get_left() + LEFT, BlockOutputText.get_left())
        BlockOutputArrow.add_updater(lambda m: m.next_to(BlockOutputText, LEFT))

        self.play(FadeIn(BlockOutputText),
                  FadeIn(BlockOutputArrow))
        
        self.wait(3)

        self.play(Box.animate.scale(2).move_to(DOWN * 0.6),
                  text.animate.scale(0.4).move_to(3.5*LEFT + UP))

        self.wait()

        subsys = VGroup()
        subsys.add(Rectangle(height=0.3, width= 0.5).move_to(3.5 * LEFT + DOWN/2))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[0], RIGHT))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[1], RIGHT))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[2], UP))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[3], UP))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[3], LEFT))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[2], RIGHT))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[6], DOWN))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[7], RIGHT))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[8], DOWN))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[6], RIGHT))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[10], RIGHT))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[11], RIGHT))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[12], UP))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[13], RIGHT))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[9], RIGHT))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[15], RIGHT))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[16], RIGHT))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[17], RIGHT))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[14], DOWN))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[19], DOWN))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[20], RIGHT))
        subsys.add(Rectangle(height=0.3, width= 0.5).next_to(subsys[21], RIGHT))

        for i in range(len(subsys)):
            self.play(Create(subsys[i]), run_time = 0.1)
        self.wait()

        ax = Axes(
            x_range=[0, 6], y_range=[0, 50, 10], axis_config={"include_tip": False}
        ).scale(0.25).move_to(3*UP)

        t = ValueTracker(0)

        def func(x):
            return 4 * (x - 3) ** 2
        graph = ax.plot(func, color=MAROON)

        initial_point = [ax.coords_to_point(t.get_value(), func(t.get_value()))]
        dot = Dot(point=initial_point)

        dot.add_updater(lambda x: x.move_to(ax.c2p(t.get_value(), func(t.get_value()))))
        x_space = np.linspace(*ax.x_range[:2],200)
        minimum_index = func(x_space).argmin()

        self.add(ax, graph, dot)
        self.wait(0.5)
        arrow_2 = Arrow(start=2.2*UP + RIGHT/2, end=UP*0.75 + RIGHT/2, color=GOLD)
        arrow_1 = Arrow(start=UP*0.75 + LEFT/2, end=UP*2.2 + LEFT/2, color=GOLD)
        self.play(GrowArrow(arrow_1), run_time = 0.5)
        self.play(FadeOut(arrow_1), GrowArrow(arrow_2), run_time = 0.5)
        self.play(FadeOut(arrow_2), run_time = 0.5)
        self.play(t.animate.set_value(x_space[minimum_index]))
        self.wait()

        self.play(FadeOut(ax),
                  FadeOut(graph),
                  FadeOut(dot),
                  FadeOut(subsys),
                  FadeOut(Box),
                  FadeOut(text),
                  FadeOut(BlockInputText),
                  FadeOut(BlockInputArrow),
                  FadeOut(BlockOutputText),
                  FadeOut(BlockOutputArrow),
                  FadeOut(airandfuel),
                  FadeOut(fuelInputArrow),
                  FadeOut(airInputArrow),)
        
        self.play(FadeIn(Text("github.com/sbguzel/car_optimization").scale(0.75)))

        self.wait()
