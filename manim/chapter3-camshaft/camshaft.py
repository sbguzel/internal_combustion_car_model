import math
from manim import *
from numpy import sin, cos
import numpy as np
import scipy.integrate as integrate

class Camshaft(Scene):
    def construct(self):
        self.camera.background_color = BURAK

        # Chapter 2
        chapterNumber = Tex("CHAPTER III").scale(3)
        chapterText = Tex("camshaft and valves").scale(1)
        chapter = VGroup(chapterNumber, chapterText).arrange(3 * DOWN)
        self.play(FadeIn(chapter[0]))
        self.play(FadeIn(chapter[1]))
        self.wait()
        self.play(FadeOut(chapter))
        self.wait()

        # What happend in C1 and C2
        crankshaftBox = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        crankshaftText = Text("Crankshaft")
        crankshaftBlock = VGroup(crankshaftBox, crankshaftText)
        crankshaftBlockInputText = Text("Torque").next_to(crankshaftBlock, LEFT * 5)
        crankshaftBlockInputArrow = Arrow(crankshaftBlockInputText.get_right(), crankshaftBox.get_left())
        thetaText = MathTex("\\theta")
        thetaDotText = MathTex("\dot{\\theta}")
        thetaDotDotText = MathTex("\ddot{\\theta}")
        crankshaftBlockOutputLine = Line(crankshaftBox.get_right(), crankshaftBox.get_right() + 2 * RIGHT)
        crankshaftOutputStateText = VGroup(thetaText, thetaDotText, thetaDotDotText).arrange(RIGHT).scale(0.75).next_to(crankshaftBlockOutputLine, UP)
        crankshaftBlackBoxGroup = VGroup(crankshaftBlockInputText, crankshaftBlockInputArrow, crankshaftBlock, crankshaftBlockOutputLine, crankshaftOutputStateText)

        # Slider-Crank Black Box
        sliderCrankBox = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        sliderCrankText = Text("Slider-Crank").scale(0.85)
        sliderCrankBlock = VGroup(sliderCrankBox, sliderCrankText)
        sliderCrankBlockOutputText1 = Text("Piston").scale(0.95)
        sliderCrankBlockOutputText2 = Text("Position").scale(0.95)
        sliderCrankBlockOutputTextGroup = VGroup(sliderCrankBlockOutputText1, sliderCrankBlockOutputText2).arrange(DOWN, center=False, aligned_edge=LEFT).next_to(sliderCrankBlock, RIGHT * 5)
        sliderCrankBlockOutputArrow = Arrow(sliderCrankBlock.get_right(), sliderCrankBlockOutputTextGroup.get_left())
        sliderCrankBlackBoxGroup = VGroup(sliderCrankBlock, sliderCrankBlockOutputArrow, sliderCrankBlockOutputTextGroup).scale(0.65).move_to(4 * RIGHT + UP)

        # Valvetrain Black Box
        valvetrainBox = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        valvetrainText = Text("Valvetrain").scale(0.85)
        valvetrainBlock = VGroup(valvetrainBox, valvetrainText)
        valvetrainBlockOutputText1 = Text("Valve").scale(0.95)
        valvetrainBlockOutputText2 = Text("Opening").scale(0.95)
        valvetrainBlockOutputTextGroup = VGroup(valvetrainBlockOutputText1, valvetrainBlockOutputText2).arrange(DOWN, center=False, aligned_edge=LEFT).next_to(valvetrainBlock, RIGHT * 5)
        valvetrainBlockOutputArrow = Arrow(valvetrainBlock.get_right(), valvetrainBlockOutputTextGroup.get_left())
        valvetrainBlackBoxGroup = VGroup(valvetrainBlock, valvetrainBlockOutputArrow, valvetrainBlockOutputTextGroup).scale(0.65).move_to(4 * RIGHT + DOWN)

        self.play(FadeIn(crankshaftBlackBoxGroup.scale(0.65).move_to(3 * LEFT)))

        self.wait()

        verticalline1 = Line(0 * UP, UP)
        arrow1 = Arrow(UP, sliderCrankBlackBoxGroup.get_left(), buff = 0, max_tip_length_to_length_ratio = 0.1, max_stroke_width_to_length_ratio=3)
        bendedArrow1 = VGroup(verticalline1, arrow1)
        self.play(FadeIn(sliderCrankBlackBoxGroup), Create(bendedArrow1))

        self.wait()

        verticalline2 = Line(0 * DOWN, DOWN)
        arrow2 = Arrow(DOWN, valvetrainBlackBoxGroup.get_left(), buff = 0, max_tip_length_to_length_ratio = 0.1, max_stroke_width_to_length_ratio=3)
        bendedArrow2 = VGroup(verticalline2, arrow2)
        self.play(FadeIn(valvetrainBlackBoxGroup), Create(bendedArrow2))

        self.play(Circumscribe(valvetrainBlackBoxGroup[0], buff = 0))

        self.wait()

        valvetrainBlockInputText = MathTex("\\theta").next_to(valvetrainBlackBoxGroup, 3 * LEFT)

        valvetrainInputArrow = Arrow(valvetrainBlockInputText.get_right(), valvetrainBlackBoxGroup.get_left(), buff = SMALL_BUFF)

        self.play(FadeOut(sliderCrankBlackBoxGroup, crankshaftBlackBoxGroup, bendedArrow1),
                  ReplacementTransform(bendedArrow2, valvetrainBlockInputText),
                  FadeIn(valvetrainInputArrow))
        
        valvetrainBlackBoxGroup.add(valvetrainBlockInputText, valvetrainInputArrow)

        self.wait()

        # Note the Valvetrain Black Box
        self.play(valvetrainBlackBoxGroup.animate.scale(0.75).to_corner(UL))
        box1 = SurroundingRectangle(valvetrainBlackBoxGroup, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box1))

        valvetrainBlackBoxGroup.add(box1)

        self.wait()

        camProfileEq = MathTex(r"e^{-(2 \cdot x - pi/2)^{4}}")

        self.play(Write(camProfileEq))

        self.wait()

        self.play(camProfileEq.animate.next_to(valvetrainBlackBoxGroup, 1.4 * RIGHT))

        box2 = SurroundingRectangle(camProfileEq, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box2))
        camProfileEqGroup = VGroup(camProfileEq, box2)

        # Cam Profile
        plane = NumberPlane(background_line_style={
            "stroke_color": WHITE,
            "stroke_width": 1,
            "stroke_opacity": 0.5
        }).set_color(DARK_BLUE)
        
        ax = Axes(
            x_range=[0, 7],
            x_length= 7,
            y_length= 2,
            y_range=[0, 2],
            axis_config={"include_tip": False}
        )

        def func(x):
            return np.power(np.e, -np.power(2 * x - PI/2, 4))
        
        graph = ax.plot(func, color=MAROON)

        self.play(FadeIn(ax, graph))

        self.wait()

        t = ValueTracker(0)
        initial_point = [ax.coords_to_point(t.get_value(), func(t.get_value()))]
        dot = Dot(point=initial_point)
        dot.add_updater(lambda x: x.move_to(ax.c2p(t.get_value(), func(t.get_value()))))
        x_space = np.linspace(*ax.x_range[:2],200)

        graph.add_updater(
            lambda gr : gr.move_to(ax.get_center() + 0.43 * DOWN + 0.06 * RIGHT)
        )

        self.play(ax.animate.move_to(2 * DOWN))

        self.wait()

        ax_polar = Axes(
            x_range=[-3, 3],
            x_length= 3,
            y_length= 3,
            y_range=[-3, 3],
            axis_config={"include_tip": False}
        )

        self.play(FadeIn(ax_polar))

        r = lambda theta: func(theta)/2 + 1
        polarGraph = plane.plot_polar_graph(r, [0, 2 * PI], color=WHITE)

        self.add(dot)
        self.play(t.animate.set_value(x_space[180]),
                  Create(polarGraph),
                  run_time = 7)
        
        self.wait()

        useCenterofGraph = Square().scale(2).set_opacity(0)

        centeredPolarGraph = VGroup(polarGraph, useCenterofGraph)

        polarCamGroup = VGroup(ax_polar, centeredPolarGraph)

        self.play(FadeOut(ax, graph, dot), polarCamGroup.animate.scale(0.5).move_to(3 * RIGHT + 2.25 * UP))

        Yoffset = 2.5 * DOWN
        Xoffset = 3 * RIGHT
        startAngle = 0
        curAngle = 0
        l1 = 0.13
        l2 = 0.44
        e = 0
        h = 0

        pistonPosition = math.sqrt(math.pow(l2,2) - math.pow(e + l1 * math.sin(0),2)) + (l1 * math.cos(0)) + h
        m2br = 5

        crank = SVGMobject(file_name = "crank.svg").rotate(startAngle).move_to(Xoffset + Yoffset)
        piston = SVGMobject(file_name = "piston.svg").scale(0.5).move_to(pistonPosition * m2br * UP + Xoffset + Yoffset)
        rod = self.getline(0*UP + 0*DOWN + Xoffset + Yoffset, piston.get_center()).set_stroke(width=50).set_opacity(0.75)
        
        self.play(FadeIn(rod), FadeIn(crank), FadeIn(piston), run_time = 0.5)
        self.wait()

        yLine = Line(crank.get_center(), piston.get_center() + 3 * UP).set_stroke(width=3, color = RED)
        xLine = Line(crank.get_center() + 3 * LEFT, crank.get_center() + 3 * RIGHT).set_stroke(width=3, color = RED)
        zero = MathTex("0^{\\circ}", stroke_width = 1).scale(0.8).set_color(RED).next_to(yLine, UP)
        temporigin = MathTex("(0,0)", stroke_width = 1).scale(0.8).set_color(RED).next_to(crank.get_center(), DOWN * 0.5)

        self.play(Create(xLine), Create(yLine), FadeIn(zero), FadeIn(temporigin))
        self.wait()

        valveLine = Line(1.75 * UP + Xoffset, UP + Xoffset).set_stroke(width=5, color = YELLOW)
        valveHead = Line(0.25 * LEFT, 0.25 * RIGHT).set_stroke(width=5, color = YELLOW).move_to(valveLine.get_end())
        valveHead.add_updater(
             lambda line : line.move_to(valveLine.get_end())
        )
        valve = VGroup(valveLine, valveHead)
        
        self.add(valve)

        self.wait()

        self.play(Rotate(polarCamGroup[1], angle= PI))

        self.wait()

        self.play(camProfileEqGroup.animate.to_edge(UP, buff = 0.35))

        gearRatio = MathTex(r"\theta_{camshaft} = \theta_{crankshaft} / 2").scale(0.5).next_to(camProfileEqGroup, DOWN)
        box3 = SurroundingRectangle(gearRatio, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(FadeIn(gearRatio))
        self.play(Create(box3))
        gearRatioGroup = VGroup(gearRatio, box3)

        self.wait()

        rod.add_updater(
            lambda mob: mob.become(self.getline(self.getPointPos(l1, curAngle, startAngle, Xoffset, Yoffset), piston.get_center()).set_stroke(width=50).set_opacity(0.75))
        )
        
        for i in range(360):
            curAngle = (2 * PI) * (i / 60) + startAngle
            pistonPosition = math.sqrt(math.pow(l2,2) - math.pow(e + l1 * math.sin(curAngle),2)) + (l1 * math.cos(curAngle)) + h
            valveModdedAngle = curAngle % (4 * PI)
            valvePosition = math.pow(math.e, -(math.pow(valveModdedAngle - PI/2, 4)))
            self.play(
                Rotate(crank, angle= 0.10472),
                piston.animate.move_to(pistonPosition * m2br * UP + Xoffset + Yoffset),
                Rotate(polarCamGroup[1], angle= 0.10472 / 2),
                valve[0].animate.move_to(valvePosition * 0.25 * DOWN + 1.35 * UP + Xoffset),
                run_time = 1/30)
        self.wait(2)

        self.play(polarCamGroup.animate.scale(0.8).next_to(gearRatioGroup, 0.25 * RIGHT).to_edge(UP, buff = 0.25),
                  FadeOut(piston, rod, crank, xLine, yLine, zero, temporigin, valve))
        
        polarCamGroup.remove(centeredPolarGraph)
        polarCamGroup.add(polarGraph)
        
        box4 = SurroundingRectangle(polarCamGroup, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box4))
        polarCamSumGroup = VGroup(polarCamGroup, box4)
                  
        self.wait()

        # Show Valve Float

        vfPlane = NumberPlane(background_line_style={
            "stroke_color": WHITE,
            "stroke_width": 1,
            "stroke_opacity": 0.5
        }).set_color(DARK_BLUE)

        self.play(FadeIn(vfPlane))

        def func(x):
            return np.power(np.e, -np.power(2 * x - PI/2, 4))
        
        r = lambda theta: func(theta)/2 + 1
        polarGraph = vfPlane.plot_polar_graph(r, [0, 2 * PI], color=WHITE)
        useCenterofGraph = Square().scale(5).set_opacity(0)
        vfCenteredPolarGraph = VGroup(polarGraph, useCenterofGraph).rotate(PI)

        self.play(FadeIn(vfCenteredPolarGraph))

        vfValveLine = Line(DOWN, 2.6 * DOWN).set_stroke(width=20, color = WHITE)
        vfValveHead = Line(0.5 * LEFT, 0.5 * RIGHT).set_stroke(width=20, color = WHITE).move_to(vfValveLine.get_end())
        tipdot = Dot(radius = 0.1)
        tipdot.add_updater(
            lambda d : d.move_to(vfValveLine.get_start())
        )
        vfValveHead.add_updater(
             lambda line : line.move_to(vfValveLine.get_end())
        )
        vfValve = VGroup(vfValveLine, vfValveHead, tipdot)
        
        self.add(vfValve)

        for i in range(60):
            curAngle = (PI / 3.5) * (i / 60)
            valvePosition = math.pow(math.e, -(math.pow(curAngle * 2 - PI/2, 4)))
            self.play(
                Rotate(vfCenteredPolarGraph, angle = (PI / 3) / 60),
                vfValve[0].animate.move_to(valvePosition * 0.55 * DOWN + 1.9 * DOWN),
                run_time = 1/20)
            
        for i in range(60):
            curAngle = (PI / 3) + (PI / 3.5) * (i / 60)
            valvePosition = math.pow(math.e, -(math.pow((curAngle * 2) - PI/2 - PI/8, 4)))
            self.play(
                Rotate(vfCenteredPolarGraph, angle = (PI / 3) / 60),
                vfValve[0].animate.move_to(valvePosition * 0.55 * DOWN + 1.9 * DOWN),
                run_time = 1/20)
            
        self.wait()

        self.play(FadeOut(vfCenteredPolarGraph, vfValve, vfPlane))

        self.wait()

        simpleModel = Dot(radius=0.3).set_color(BLUE)

        self.add(simpleModel)

        spring = Spring(2.25 * DOWN, 4).rotate(PI/2).set_opacity(0)

        def springupdater(m: Spring):
            # Modified Mobject.put_start_and_end_on
            curr_start, curr_end = m.get_start_and_end()
            curr_vect = curr_end - curr_start
            target_vect = (
                (2 + simpleModel.get_y()) * UP
            )
            m.stretch(
                np.linalg.norm(target_vect) / np.linalg.norm(curr_vect),
                1,
                about_point=curr_start,
            )
            m.move_to(2.25 * DOWN + (2 + simpleModel.get_y()) / 2 * UP)

        spring.add_updater(springupdater)

        self.add(spring)

        m = 0.1
        k = 1
        b = 0.1
        f = 0

        def derivs(state, t):
            dydx = np.zeros_like(state)

            dydx[0] = state[1]
            dydx[1] = (-k/m) * state[0] - (b/m) * state[1] + (1/m) * f

            return dydx

        dt = 0.05
        t = np.arange(0, 6, dt)

        pos = -1.0
        vel = 0.0

        state = ([pos, vel])

        y = integrate.odeint(derivs, state, t)

        px = y[:, 0]
        v = y[:, 1]

        virtualcam = Line(0.4 * LEFT, 0.4 * RIGHT).set_stroke(width=20).move_to(0.4 * UP)

        self.add(virtualcam)

        self.wait()

        spring.set_opacity(1)
        
        self.play(simpleModel.animate.move_to(px[0]*UP), virtualcam.animate.move_to(virtualcam.get_center() + DOWN))

        self.wait()

        self.play(virtualcam.animate.move_to(0.4 * UP))

        for i in range(len(px)-1):
            self.play(
                AnimationGroup(
                    simpleModel.animate.move_to(px[i]*UP),
                    run_time=1/20,
                    rate_func=linear,
                    lag_ratio=0
                )
                )

        self.wait()

        self.play(FadeOut(simpleModel, virtualcam, spring))

        stateSpaceTex = VGroup(MathTex("\dot{x}", "=", "A", "\\cdot",  "x",  "+", "B", "\\cdot", "u"), MathTex("y", "=", "C", "\\cdot", "x", "+", "D", "\\cdot", "u")).scale(1.1).arrange(DOWN, center=True)

        self.play(FadeIn(stateSpaceTex))

        self.wait()

        stateSpaceTex2 = VGroup(MathTex("\\begin{bmatrix} \\dot{x} \\\ \\ddot{x} \end{bmatrix}", "=", "A", "\\cdot",  "x",  "+", "B", "\\cdot", "u"), MathTex("y", "=", "C", "\\cdot", "x", "+", "D", "\\cdot", "u")).scale(1.1).arrange(DOWN, center=True)

        self.play(stateSpaceTex.animate.become(stateSpaceTex2))

        self.wait()

        stateSpaceTex3 = VGroup(MathTex("\\begin{bmatrix} \\dot{x} \\\ \\ddot{x} \end{bmatrix}", "=", "\\begin{bmatrix} 0 & 1 \\\ -\\frac{k}{m} & -\\frac{c}{m} \end{bmatrix}", "\\cdot",  "x",  "+", "B", "\\cdot", "u"), MathTex("y", "=", "C", "\\cdot", "x", "+", "D", "\\cdot", "u")).scale(1.1).arrange(DOWN, center=True)

        self.play(stateSpaceTex.animate.become(stateSpaceTex3))

        self.wait()

        stateSpaceTex4 = VGroup(MathTex("\\begin{bmatrix} \\dot{x} \\\ \\ddot{x} \end{bmatrix}", "=", "\\begin{bmatrix} 0 & 1 \\\ -\\frac{k}{m} & -\\frac{c}{m} \end{bmatrix}", "\\cdot",  "\\begin{bmatrix} x \\\ \\dot{x} \end{bmatrix}",  "+", "B", "\\cdot", "u"), MathTex("y", "=", "C", "\\cdot", "x", "+", "D", "\\cdot", "u")).scale(1.1).arrange(DOWN, center=True)

        self.play(stateSpaceTex.animate.become(stateSpaceTex4))

        self.wait()

        stateSpaceTex5 = VGroup(MathTex("\\begin{bmatrix} \\dot{x} \\\ \\ddot{x} \end{bmatrix}", "=", "\\begin{bmatrix} 0 & 1 \\\ -\\frac{k}{m} & -\\frac{c}{m} \end{bmatrix}", "\\cdot",  "\\begin{bmatrix} x \\\ \\dot{x} \end{bmatrix}"), MathTex("y", "=", "C", "\\cdot", "x")).scale(1.1).arrange(DOWN, center=True)

        self.play(TransformMatchingShapes(stateSpaceTex, stateSpaceTex5))

        self.wait()

        stateSpaceTexFinal = MathTex("\\begin{bmatrix} \\dot{x} \\\ \\ddot{x} \end{bmatrix}", "=", "\\begin{bmatrix} 0 & 1 \\\ -\\frac{k}{m} & -\\frac{c}{m} \end{bmatrix}", "\\cdot",  "\\begin{bmatrix} x \\\ \\dot{x} \end{bmatrix}").scale(1.1)

        self.play(TransformMatchingShapes(stateSpaceTex5, stateSpaceTexFinal))

        self.wait()

        self.play(stateSpaceTexFinal.animate.scale(0.68).to_corner(UR))

        box5 = SurroundingRectangle(stateSpaceTexFinal, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box5))
        stateSpaceTexGroup = VGroup(stateSpaceTexFinal, box5)

        self.wait()

        matlabExample = Text("MATLAB Example").scale(0.85)

        self.play(FadeIn(matlabExample))

        self.wait()

        self.play(FadeOut(matlabExample))

        csExample = Text("C# Example").scale(0.85)

        self.play(FadeIn(csExample))

        self.wait()

        self.play(FadeOut(csExample))

        self.wait()

        self.play(FadeOut(stateSpaceTexGroup, polarCamSumGroup, valvetrainBlackBoxGroup, camProfileEqGroup, gearRatioGroup))

        nextChapterText = Tex("Next Chapter").scale(2)
        nextChapterTopic = Tex("thermodynamics")
        nextChapter = VGroup(nextChapterText, nextChapterTopic).arrange(1.5 * DOWN)
        self.play(FadeIn(nextChapter))
        self.wait()
        self.play(FadeOut(nextChapter))
        self.wait()



    def getline(self, Point1, Point2):
        line = Line(Point1,Point2)
        return line
    
    def getPointPos(self, l1, curAngle, startAngle, Xoffset, Yoffset):
            curAngle += PI/30
            crankXpos = (l1 * 5) * math.cos(curAngle - startAngle)
            crankYpos = -(l1 * 5) * math.sin(curAngle - startAngle)
            return crankXpos * UP + crankYpos * RIGHT + Xoffset + Yoffset


class Spring(VMobject):
    def __init__(self, start=ORIGIN, length=2, bumps=14):
        self.length = length
        self.empty = 0.4
        self.step = 0.07
        self.bump = 0.18
        super().__init__(color=WHITE)
        vertices = np.array(
            [
                [0, 0, 0],
                [self.empty, 0, 0],
                [self.empty + self.step, self.bump, 0],
                *[
                    [
                        self.empty + self.step + self.step * 2 * i,
                        self.bump * (1 - (i % 2) * 2),
                        0,
                    ]
                    for i in range(1, bumps)
                ],
                [self.empty + self.step * 2 * bumps, 0, 0],
                [self.empty * 2 + self.step * 2 * bumps, 0, 0],
            ]
        )
        vertices = vertices * [self.length /
                               (1 + 0.2 * bumps), 1, 0] + np.array(start)

        self.start_new_path(np.array(start))
        self.add_points_as_corners(
            [*(np.array(vertex) for vertex in vertices)])