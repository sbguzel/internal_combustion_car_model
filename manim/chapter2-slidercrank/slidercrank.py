import math
from manim import *

class SliderCrank(Scene):
    def construct(self):
        self.camera.background_color = BURAK

        # Chapter 2
        chapterNumber = Tex("CHAPTER II").scale(3)
        chapterText = Tex("slider-crank mechanism").scale(1)
        chapter = VGroup(chapterNumber, chapterText).arrange(3 * DOWN)
        self.play(FadeIn(chapter[0]))
        self.play(FadeIn(chapter[1]))
        self.wait()
        self.play(FadeOut(chapter))
        self.wait()

        # What happend in C1
        crankshaftBox = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        crankshaftText = Text("Crankshaft")
        crankshaftBlock = VGroup(crankshaftBox, crankshaftText)
        crankshaftBlockInputText = Text("Torque").next_to(crankshaftBlock, LEFT * 5)
        crankshaftBlockInputArrow = Arrow(crankshaftBlockInputText.get_right(), crankshaftBox.get_left())
        thetaText = MathTex("\\theta")
        thetaDotText = MathTex("\dot{\\theta}")
        thetaDotDotText = MathTex("\ddot{\\theta}")
        crankshaftOutputStateText = VGroup(thetaText, thetaDotText, thetaDotDotText).arrange(DOWN, center=False, aligned_edge=LEFT).next_to(crankshaftBlock, RIGHT * 6)
        crankshaftBlockOutputArrow = Arrow(crankshaftBox.get_right(), crankshaftOutputStateText.get_left())
        crankshaftBlackBoxGroup = VGroup(crankshaftBlockInputText, crankshaftBlockInputArrow, crankshaftBlock, crankshaftBlockOutputArrow, crankshaftOutputStateText)
        self.play(FadeIn(crankshaftBlackBoxGroup))
        self.wait()

        # Prepare for new Black Box
        self.play(crankshaftBlackBoxGroup[4].animate.arrange(RIGHT).scale(0.75).next_to(crankshaftBlackBoxGroup[3], UP))
        self.wait()
        self.play(crankshaftBlackBoxGroup.animate.scale(0.75).move_to(3 * LEFT))
        self.wait()

        # Slider-Crank Black Box
        sliderCrankBox = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        sliderCrankText = Text("Slider-Crank").scale(0.85)
        sliderCrankBlock = VGroup(sliderCrankBox, sliderCrankText)
        sliderCrankBlockOutputText1 = Text("Piston").scale(0.95)
        sliderCrankBlockOutputText2 = Text("Position").scale(0.95)
        sliderCrankBlockOutputTextGroup = VGroup(sliderCrankBlockOutputText1, sliderCrankBlockOutputText2).arrange(DOWN, center=False, aligned_edge=LEFT).next_to(sliderCrankBlock, RIGHT * 5)
        sliderCrankBlockOutputArrow = Arrow(sliderCrankBlock.get_right(), sliderCrankBlockOutputTextGroup.get_left())
        sliderCrankBlackBoxGroup = VGroup(sliderCrankBlock, sliderCrankBlockOutputArrow, sliderCrankBlockOutputTextGroup).scale(0.75).next_to(crankshaftBlackBoxGroup, RIGHT)
        
        self.play(FadeIn(sliderCrankBlackBoxGroup))
        self.play(Circumscribe(sliderCrankBlock, buff = 0))
        self.wait()

        # Change input and output variables for Slider-Crank Black Box
        sliderCrankBlockInputText = MathTex("\\theta").next_to(crankshaftBlockOutputArrow, LEFT)

        crankshaftBlackBoxGroup.remove(crankshaftBlockOutputArrow)
        sliderCrankBlackBoxGroup.add(crankshaftBlockOutputArrow)
        sliderCrankBlackBoxGroup.add(sliderCrankBlockInputText)

        self.play(ReplacementTransform(crankshaftBlackBoxGroup, sliderCrankBlockInputText))

        newOutputText = MathTex("y").move_to(sliderCrankBlockOutputTextGroup.get_left() + 0.2 * RIGHT)
        self.play(ReplacementTransform(sliderCrankBlockOutputTextGroup, newOutputText))

        sliderCrankBlackBoxGroup.remove(sliderCrankBlockOutputTextGroup)
        sliderCrankBlackBoxGroup.add(newOutputText)

        # Note the Slider-Crank Black Box
        self.play(sliderCrankBlackBoxGroup.animate.scale(0.75).to_corner(UL))
        box1 = SurroundingRectangle(sliderCrankBlackBoxGroup, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box1))
        sliderCrankBlackBoxGroup.add(box1)
        self.wait()

         # Show Crank-Piston Cycle
        Xoffset = 2 * DOWN
        startAngle = 0
        curAngle = 0
        l1 = 0.13
        l2 = 0.44
        e = 0
        d = math.sqrt(math.pow(l2 - l1, 2) - math.pow(e,2))

        crank = SVGMobject(file_name = "crank.svg").rotate(startAngle).move_to(Xoffset)
        piston = SVGMobject(file_name = "piston.svg").scale(0.5).move_to(((2*l1)*5+1.5)*UP + Xoffset)
        rod = self.getline(0*UP + 0*DOWN + Xoffset, piston.get_center()).set_stroke(width=50).set_opacity(0.75)

        self.play(FadeIn(rod), FadeIn(crank), FadeIn(piston), run_time = 0.5)
        self.wait()

        showAngleLine = Line(2 * DOWN, 0.5 * DOWN).set_stroke(width=2, color = BLACK).set_opacity(0.75)

        showAngleLineText = MathTex("\\theta", stroke_width = 2).scale(0.75).set_color(BLACK).move_to(showAngleLine.get_end())

        showAngleLineText.add_updater(
            lambda tex: tex.become(MathTex("\\theta", stroke_width = 2).scale(0.75).set_color(BLACK).move_to(showAngleLine.get_end()))
        )

        self.add(showAngleLine)

        yLine = Line(crank.get_center(), piston.get_center() + 2 * UP).set_stroke(width=3, color = RED)
        xLine = Line(crank.get_center() + 3 * LEFT, crank.get_center() + 3 * RIGHT).set_stroke(width=3, color = RED)
        
        zero = MathTex("0^{\\circ}", stroke_width = 1).scale(0.8).set_color(RED).next_to(yLine, UP)
        temporigin = MathTex("(0,0)", stroke_width = 1).scale(0.8).set_color(RED).next_to(crank.get_center(), DOWN * 0.5)

        self.play(Create(xLine), Create(yLine))
        self.wait()
        self.play(FadeIn(zero), FadeIn(temporigin))

        pistonTipLine = Line(piston.get_top() + 2 * LEFT, piston.get_top()).set_stroke(width=1).set_opacity(0.75)

        pistonTipLine.add_updater(
            lambda line: line.become(Line(piston.get_top() + 2 * LEFT, piston.get_top()).set_stroke(width=1).set_opacity(0.75))
        )

        pistonTipArrow = Arrow(2 * DOWN + 2 * LEFT, piston.get_top() + 2 * LEFT, stroke_width=2, max_tip_length_to_length_ratio=0.2, buff = 0).set_opacity(0.75)

        pistonTipArrow.add_updater(
            lambda arrow: arrow.become(Arrow(2 * DOWN + 2 * LEFT, piston.get_top() + 2 * LEFT, stroke_width=2, max_tip_length_to_length_ratio=0.2, buff = 0).set_opacity(0.75))
        )

        yText = MathTex("y")

        yText.add_updater(
            lambda tex: tex.next_to(pistonTipArrow, 0.5 * LEFT)
        )

        self.play(Create(pistonTipLine), run_time = 0.25)
        self.play(Create(pistonTipArrow), FadeIn(yText))

        showAngle = Arc(angle = 0)

        self.add(showAngle)

        rod.add_updater(
            lambda mob: mob.become(self.getline(self.getPointPos(l1, curAngle, startAngle, Xoffset),piston.get_center()).set_stroke(width=50).set_opacity(0.75))
        )

        self.add(showAngleLineText)
        
        for i in range(60):
            curAngle = (2 * PI) * (i / 60) + startAngle
            pistonPosition = math.sqrt(math.pow(l2,2) - math.pow(e + l1 * math.cos(curAngle + PI/2),2)) + (l1 * math.sin(curAngle + PI/2)) - d
            self.play(
                Rotate(crank, angle= 0.10472),
                Rotate(showAngleLine, angle= 0.10472, about_point = 2 * DOWN + 0 * LEFT),
                showAngle.animate.become(Arc(radius = 1.2, angle = curAngle + PI/30, start_angle= PI/2).move_arc_center_to(2 * DOWN).set_color(BLACK)),
                piston.animate.move_to(((pistonPosition * 5) + 1.5) * UP + Xoffset),
                run_time = 1/15)
        self.wait(2)

        # add e

        e = 0.05
        d = math.sqrt(math.pow(l2 - l1, 2) - math.pow(e,2))

        eline = Line(2 * DOWN, 2.5 * UP).set_stroke(width=1).set_opacity(0.75)

        eline.add_updater(
            lambda line: line.become(Line(2 * DOWN + piston.get_x() * RIGHT, 2.5 * UP + piston.get_x() * RIGHT).set_stroke(width=1).set_opacity(0.75))
        )

        self.add(eline)

        pistonTipLine.add_updater(
            lambda line: line.become(Line(piston.get_top() + (piston.get_x() + 2) * LEFT, piston.get_top()).set_stroke(width=1).set_opacity(0.75))
        )
        pistonTipArrow.add_updater(
            lambda arrow: arrow.become(Arrow(2 * DOWN + 2 * LEFT, piston.get_top() + (2 + piston.get_x()) * LEFT, stroke_width=2, max_tip_length_to_length_ratio=0.2, buff = 0).set_opacity(0.75))
        )

        self.play(piston.animate.move_to(((pistonPosition * 5) + 1.5) * UP + Xoffset + e * 5 * RIGHT))

        earrow1 = Arrow(0.5 * LEFT + 1.5 * UP, 0 * LEFT + 1.5 * UP, buff = 0)
        earrow2 = Arrow((e * 5 + 0.5) * RIGHT + 1.5 * UP, e * 5 * RIGHT + 1.5 * UP, buff = 0)
        etext = MathTex("e").scale(0.75).next_to(earrow2, UR * 0.25)
        self.play(FadeIn(earrow1, earrow2, etext))

        for i in range(60):
            curAngle = (2 * PI) * (i / 60) + startAngle
            pistonPosition = math.sqrt(math.pow(l2,2) - math.pow(e + l1 * math.cos(curAngle + PI/2),2)) + (l1 * math.sin(curAngle + PI/2)) - d
            self.play(
                Rotate(crank, angle= 0.10472),
                Rotate(showAngleLine, angle= 0.10472, about_point = 2 * DOWN + 0 * LEFT),
                showAngle.animate.become(Arc(radius = 1.2, angle = curAngle + PI/30, start_angle= PI/2).move_arc_center_to(2 * DOWN).set_color(BLACK)),
                piston.animate.move_to(((pistonPosition * 5) + 1.5) * UP + Xoffset + e * 5 * RIGHT),
                run_time = 1/30)
        self.wait(2)

        # Go to 30 Degree For Geometry

        for i in range(8):
            curAngle = (2 * PI) * (i / 60) + startAngle
            pistonPosition = math.sqrt(math.pow(l2,2) - math.pow(e + l1 * math.cos(curAngle + PI/2),2)) + (l1 * math.sin(curAngle + PI/2)) - d
            self.play(
                Rotate(crank, angle= 0.10472),
                Rotate(showAngleLine, angle= 0.10472, about_point = 2 * DOWN + 0 * LEFT),
                showAngle.animate.become(Arc(radius = 1.2, angle = curAngle + PI/30, start_angle= PI/2).move_arc_center_to(2 * DOWN).set_color(BLACK)),
                piston.animate.move_to(((pistonPosition * 5) + 1.5) * UP + Xoffset + e * 5 * RIGHT),
                run_time = 1/30)
        self.wait(2)

        # Convert Models to Lines

        crankpistonmodel = VGroup(piston, rod, crank)

        point1 = Dot(point = 2 * DOWN, radius = 0.08)
        point2 = Dot(point = self.getPointPos(l1, curAngle, startAngle, Xoffset), radius = 0.08)
        point3 = Dot(point = piston.get_top() + DOWN/2, radius = 0.08)

        line_1 = Line(point1.get_center(), point2.get_center()).set_stroke(width=5)
        line_2 = Line(point2.get_center(), point3.get_center()).set_stroke(width=5)

        lineModelGroup = VGroup(line_1, line_2, point1, point2, point3)

        p1 = [piston.get_x(), piston.get_y(), 0]
        p2 = [piston.get_x(), piston.get_y() + 0.5, 0]
        pistonLengthBrace = BraceBetweenPoints(p1,p2, buff = 0)
        pistonLengthTex = Tex("h").next_to(pistonLengthBrace, RIGHT, SMALL_BUFF)

        pistonLengthGroup = VGroup(pistonLengthBrace, pistonLengthTex)

        self.add(lineModelGroup, pistonLengthGroup)

        for i in range(3):
            self.play(FadeOut(crankpistonmodel[i]), run_time = 0.2)

        self.wait()

        # Focus
        yText.clear_updaters()
        eline.clear_updaters()
        etext.clear_updaters()
        pistonTipLine.clear_updaters()
        showAngleLineText.clear_updaters()

        self.play(eline.animate.become(Line(2 * DOWN + e * 5 * RIGHT, point3.get_center()).set_stroke(width=1).set_opacity(0.75)),
                  pistonTipLine.animate.become(Line(point3.get_center(), point3.get_center() + e * 5 * LEFT)).set_stroke(width=1).set_opacity(0.75),
                  FadeOut(pistonTipArrow, earrow1, earrow2, showAngle, showAngleLine, pistonLengthGroup))
        
        thetaAngle = Angle(line_1, yLine, other_angle=True, radius=0.4)

        yText.become(MathTex("y-h").scale(0.75).move_to(yText.get_center()))

        self.play(FadeIn(thetaAngle),
                  etext.animate.next_to(pistonTipLine, UP),
                  yText.animate.next_to(eline, RIGHT),
                  showAngleLineText.animate.become(MathTex("\\theta").scale(0.75).set_color(WHITE).next_to(thetaAngle, 0.2 * UP)))
                
        self.wait()

        position_list = [
            [0, -2, 0],
            [point2.get_x(), point2.get_y(), 0],
            [point3.get_x(), point3.get_y(), 0],
            [e*5, -2, 0],
        ]
        poly = Polygon(*position_list).set_fill(BLUE,opacity=0.5).set_stroke(width=1)

        self.play(FadeIn(poly))

        self.wait()

        plane = NumberPlane(background_line_style={
                "stroke_color": RED,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }).move_to(2 * DOWN).set_color(RED)
        
        self.play(FadeOut(lineModelGroup, eline, pistonTipLine))

        self.wait()
        
        self.play(Create(plane), temporigin.animate.scale(0.75).move_to(2.2 * DOWN + 0.5 * LEFT))

        self.wait()

        # Expand Shape
        
        position_list_2 = [
            [0, -2, 0],
            [-2, -1, 0],
            [1, 2, 0],
            [1, -2, 0],
        ]

        modifiedPoly = Polygon(*position_list_2).set_fill(BLUE,opacity=0.5).set_stroke(width=1)
        

        center_vertices = modifiedPoly.get_center_of_edges_outside()

        labels = VGroup(*[
            MathTex(label).move_to(point) for label,point in zip(["l_1","l_2","y-h", "e"],center_vertices)
            ])
        
        labels[2].move_to(1.75 * RIGHT)

        self.play(poly.animate.become(modifiedPoly),
                 thetaAngle.animate.become(Angle(Line(2.5 * DOWN + RIGHT, 2 * LEFT + DOWN), Line(0 * DOWN, 3 * DOWN), quadrant=(1,-1), other_angle = True, radius=0.4))
)

        self.bring_to_front(thetaAngle, showAngleLineText)

        oldTextGroup = VGroup(etext, yText)

        self.play(TransformMatchingTex(oldTextGroup,labels))

        self.wait()

        # Start Calculation

        line1 = Line(2 * DOWN, DOWN + 2 * LEFT).set_color(YELLOW).set_stroke(width=4)
        line1_cos = Line(2 * DOWN, DOWN).set_color(YELLOW).set_stroke(width=4)

        self.play(Create(line1))

        self.wait()

        self.play(line1.animate.become(line1_cos))

        self.play(line1.animate.move_to(1.5 * DOWN + RIGHT))

        self.wait()

        p1 = [1,-2,0]
        p2 = [1,-1,0]
        brace1 = BraceBetweenPoints(p1,p2, buff = 0)

        l1cos = MathTex(r"l_1 \cdot \cos\theta").scale(0.75).next_to(brace1, RIGHT, SMALL_BUFF)

        self.play(FadeIn(brace1), FadeOut(line1), FadeIn(l1cos))

        self.wait()

        p1 = [1,-1,0]
        p2 = [1,2,0]
        brace2 = BraceBetweenPoints(p1,p2, buff = 0)
        yminusl1cos = MathTex(r"y - h - l_1 \cdot \cos\theta").scale(0.75).next_to(brace2, RIGHT, SMALL_BUFF)
        pythagoras1 = VGroup(brace2, yminusl1cos)
        self.play(ReplacementTransform(labels[2], pythagoras1))

        self.wait()
        
        self.play(FadeOut(l1cos, brace1))

        self.wait()

        line2 = Line(2 * DOWN, DOWN + 2 * LEFT).set_color(YELLOW).set_stroke(width=4)
        line2_sin = Line(DOWN, DOWN + 2 * LEFT).set_color(YELLOW).set_stroke(width=4)

        self.play(Create(line2))

        self.wait()

        self.play(line2.animate.become(line2_sin))

        self.wait()

        p1 = [-2,-1,0]
        p2 = [0,-1,0]
        brace3 = BraceBetweenPoints(p1,p2, buff = 0)

        l1sin = MathTex(r"l_1 \cdot \sin\theta").scale(0.75).next_to(brace3, DOWN, SMALL_BUFF)

        self.play(FadeIn(brace3, l1sin), FadeOut(line2, thetaAngle, showAngleLineText, labels[0]))

        self.wait()

        p1 = [-2,-1,0]
        p2 = [1,-1,0]
        brace4 = BraceBetweenPoints(p1,p2, buff = 0)

        l1sin_e = MathTex(r"l_1 \cdot \sin\theta + e").scale(0.75).next_to(brace4, DOWN, SMALL_BUFF)

        self.play(brace3.animate.become(brace4), TransformMatchingTex(l1sin, l1sin_e))

        self.wait()

        tripoints = [
            [-2, -1, 0],
            [1, -1, 0],
            [1, 2, 0],
        ]

        showTriangle = Polygon(*tripoints).set_stroke(color = YELLOW, width=4)

        self.play(FadeIn(showTriangle))
        self.wait(0.5)
        self.play(FadeOut(showTriangle))

        self.wait()

        # Write Equation

        pythagorasEq = MathTex(r"(y-h-l_1\cdot\cos\theta)^2 + (l_1\cdot\sin\theta+e)^2 = l_2^2").move_to(3.25 * DOWN)

        self.play(Write(pythagorasEq))

        self.wait()

        self.play(FadeOut(plane, xLine, yLine, temporigin, zero, brace3, l1sin_e, pythagoras1, poly, labels[1], labels[3]),
                  pythagorasEq.animate.move_to(0))

        self.wait()

        pythagorasEq2 = MathTex(r"(y-h-l_1\cdot\cos\theta)^2 = l_2^2 - (l_1\cdot\sin\theta+e)^2")

        self.play(TransformMatchingTex(pythagorasEq, pythagorasEq2))
        self.wait()

        pythagorasEq3 = MathTex(r"y-h-l_1\cdot\cos\theta = \sqrt{l_2^2 - (l_1\cdot\sin\theta+e)^2}")

        self.play(TransformMatchingTex(pythagorasEq2, pythagorasEq3))
        self.wait()

        angle_to_y_eq = MathTex(r"y = \sqrt{l_2^2 - (l_1\cdot\sin\theta+e)^2} + l_1\cdot\cos\theta + h")

        self.play(TransformMatchingTex(pythagorasEq3, angle_to_y_eq))
        self.wait()

        # Note the parameters

        l1tex = MathTex("l_1 = \, stroke / 2")
        l2tex = MathTex("l_2 = \, rod \,\, length")
        thtex = MathTex("e = \, piston \,\, \\textit{offset}")
        
        parameterGroup = VGroup(l1tex, l2tex, thtex).arrange(DOWN, center= False, aligned_edge=LEFT)
        box2 = SurroundingRectangle(parameterGroup, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)

        parametersNoteGroup = VGroup(parameterGroup, box2).scale(0.62).next_to(box1)

        self.play(FadeIn(parametersNoteGroup))

        self.wait()

        # Note the angle to y

        comment = Tex("(h = length from the pin to the top of the piston)").scale(0.75)

        angle_to_y_group = VGroup(angle_to_y_eq, comment).arrange(DOWN)

        self.play(TransformMatchingTex(angle_to_y_eq, angle_to_y_group))

        self.play(angle_to_y_group.animate.scale(0.69).next_to(box2, RIGHT))

        box3 = SurroundingRectangle(angle_to_y_group, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        equationNoteGroup = VGroup(angle_to_y_group, box3)

        self.play(Create(box3))

        self.wait()

        # Parametric System

        number_plane = NumberPlane(
            x_range=(-21, 9, 1),
            y_range=(-7, 17, 1),
            x_length=7.5,
            y_length=6,
        ).move_to(DOWN + 3.5 * LEFT).set_opacity(0.25)

        self.play(Create(number_plane))

        self.wait()

        l1 = 0.04
        l2 = 0.07
        e = 0
        h = 0

        l1value = MathTex(r"l_1 = 0.04 \, m")
        l2value = MathTex(r"l_2 = 0.07 \, m")
        evalue = MathTex(r"e = 0 \, m")
        hvalue = MathTex(r"h = 0 \, m")

        values = VGroup(l1value, l2value, evalue, hvalue).arrange(DOWN, center = False, aligned_edge = LEFT).scale(0.75).move_to(5.5 * LEFT + UP)

        self.add(values)

        self.wait()

        scaleValue = 0.25

        centerDot = Dot(point = 2.25 * DOWN + 2 * LEFT, radius = 0.05)

        new_center = centerDot.get_center()

        line_1 = self.getline(new_center, new_center + scaleValue * l1 * 100 * UP).set_stroke(color = RED)

        line_2 = self.getline(new_center + scaleValue * l1 * 100 * UP, new_center + scaleValue * (l1 + l2) * 100 * UP).set_stroke(color = PINK)

        self.add(centerDot, line_1, line_2)

        self.wait()

        pistonPosition = math.sqrt(math.pow(l2,2) - math.pow(e + l1 * math.sin(0),2)) + (l1 * math.cos(0)) + h

        line_2.add_updater(
            lambda line: line.become(self.getline(line_1.get_end(), new_center + pistonPosition * 100 * UP * scaleValue))
        )

        for i in range(60):
            curAngle = (2 * PI) * (i / 60)
            pistonPosition = math.sqrt(math.pow(l2,2) - math.pow(e + l1 * math.sin(curAngle),2)) + (l1 * math.cos(curAngle)) + h
            self.play(
                Rotate(line_1, angle= 0.10472, about_point = new_center),
                run_time = 1/30)
        self.wait(2)




    def getline(self, Point1, Point2):
        line = Line(Point1,Point2)
        return line

    def getPointPos(self, l1, curAngle, startAngle, Xoffset):
            curAngle += PI/30
            crankXpos = (l1 * 5) * math.cos(curAngle - startAngle)
            crankYpos = -(l1 * 5) * math.sin(curAngle - startAngle)
            return crankXpos * UP + crankYpos * RIGHT + Xoffset


class Section(Scene):
    def construct(self):
        
        # Parametric System

        number_plane = NumberPlane(
            x_range=(-15, 9, 1),
            y_range=(-7, 17, 1),
            x_length=6,
            y_length=6,
        ).move_to(DOWN + 4 * LEFT).set_opacity(0.25)

        self.play(Create(number_plane))

        self.wait()

        l1 = 0.04
        l2 = 0.07
        e = 0
        h = 0

        l1value = MathTex(r"l_1 = 0.04 \, m")
        l2value = MathTex(r"l_2 = 0.07 \, m")
        evalue = MathTex(r"e = 0 \, m")
        hvalue = MathTex(r"h = 0 \, m")

        values = VGroup(l1value, l2value, evalue, hvalue).arrange(DOWN, center = False, aligned_edge = LEFT).scale(0.75).move_to(5.5 * LEFT + UP)

        self.add(values)

        self.wait()

        scaleValue = 0.25

        centerDot = Dot(point = 2.25 * DOWN + 3.25 * LEFT, radius = 0.05)

        new_center = centerDot.get_center()

        line_1 = self.getline(new_center, new_center + scaleValue * l1 * 100 * UP).set_stroke(color = RED)

        line_2 = self.getline(new_center + scaleValue * l1 * 100 * UP, new_center + scaleValue * (l1 + l2) * 100 * UP).set_stroke(color = PINK)

        self.add(centerDot, line_1, line_2)

        self.wait()

        i = 0
        pistonPosition = math.sqrt(math.pow(l2,2) - math.pow(e + l1 * math.sin(0),2)) + (l1 * math.cos(0)) + h
        old_pistonPosition = pistonPosition

        line_2.add_updater(
            lambda line: line.become(self.getline(line_1.get_end(), new_center + pistonPosition * 100 * UP * scaleValue + e * 100 * scaleValue * RIGHT).set_stroke(color = PINK))
        )

        self.show_axis(new_center[1])

        graph_1 = VGroup()
        
        refLine = Line(np.array([0, 0, 0]), np.array([0, 0, 0]))

        refLine.add_updater(
            lambda line: line.become(Line(np.array([new_center[0] + e * 100 * scaleValue, new_center[1] + pistonPosition * 100  * scaleValue , 0]), np.array([i/10, new_center[1] + pistonPosition * 100  * scaleValue, 0])).set_opacity(0.5))
        )
        
        self.add(refLine)

        for i in range(60):
            curAngle = (2 * PI) * (i / 60)
            pistonPosition = math.sqrt(math.pow(l2,2) - math.pow(e + l1 * math.sin(curAngle),2)) + (l1 * math.cos(curAngle)) + h
            self.play(
                Rotate(line_1, angle= 0.10472, about_point = new_center),
                run_time = 1/30)
            
            graph_1.add(Line(np.array([i/10, new_center[1] + old_pistonPosition * 100  * scaleValue, 0]), np.array([(i+1)/10, new_center[1] + pistonPosition * 100 * scaleValue, 0])))
            
            self.add(graph_1[i])
            old_pistonPosition = pistonPosition

        self.wait(2)

        # Example 2

        l1 = 0.04
        l2 = 0.07
        e = 0.015
        h = 0

        l1value = MathTex(r"l_1 = 0.04 \, m")
        l2value = MathTex(r"l_2 = 0.07 \, m")
        evalue = MathTex(r"e = 0.015 \, m")
        hvalue = MathTex(r"h = 0 \, m")

        newvalues = VGroup(l1value, l2value, evalue, hvalue).arrange(DOWN, center = False, aligned_edge = LEFT).scale(0.75).move_to(5.5 * LEFT + UP)

        new_line_1 = self.getline(new_center, new_center + scaleValue * l1 * 100 * UP).set_stroke(color = RED)

        i = 0
        pistonPosition = math.sqrt(math.pow(l2,2) - math.pow(e + l1 * math.sin(0),2)) + (l1 * math.cos(0)) + h
        old_pistonPosition = pistonPosition

        self.play(values.animate.become(newvalues),
                  line_1.animate.become(new_line_1))
        
        self.wait()

        for i in range(60):
            curAngle = (2 * PI) * (i / 60)
            pistonPosition = math.sqrt(math.pow(l2,2) - math.pow(e + l1 * math.sin(curAngle),2)) + (l1 * math.cos(curAngle)) + h
            self.play(
                Rotate(line_1, angle= 0.10472, about_point = new_center),
                run_time = 1/30)
            
            graph_1.add(Line(np.array([i/10, new_center[1] + old_pistonPosition * 100  * scaleValue, 0]), np.array([(i+1)/10, new_center[1] + pistonPosition * 100 * scaleValue, 0])).set_stroke(color = YELLOW))
            
            self.add(graph_1[60 + i])
            old_pistonPosition = pistonPosition

        
        self.wait()


        
        

    def show_axis(self, ypos):
        x_start = np.array([0,ypos,0])
        x_end = np.array([7,ypos,0])

        y_start = np.array([0,ypos - 2,0])
        y_end = np.array([0,ypos + 4,0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        self.add(x_axis, y_axis)
        self.add_x_labels(ypos)

        self.origin_point = np.array([0,ypos,0])
        self.curve_start = np.array([0,ypos,0])

    def add_x_labels(self, ypos):
        x_labels = [
            MathTex("\pi"), MathTex("2 \pi")
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([3 + 3*i, ypos, 0]), DOWN)
            self.add(x_labels[i])



    def getline(self, Point1, Point2):
        line = Line(Point1,Point2)
        return line

    def getPointPos(self, l1, curAngle, startAngle, Xoffset):
            curAngle += PI/30
            crankXpos = (l1 * 5) * math.cos(curAngle - startAngle)
            crankYpos = -(l1 * 5) * math.sin(curAngle - startAngle)
            return crankXpos * UP + crankYpos * RIGHT + Xoffset



class Polygon(Polygon):
    def get_center_of_edges_outside(self,buff=SMALL_BUFF*3):
        vertices = self.get_vertices()
        coords_vertices = []
        for i in range(len(vertices)):
            if i < len(vertices)-1:
                p1,p2 = [vertices[i],vertices[i+1]]
            else:
                p1,p2 = [vertices[-1],vertices[0]]
            guide_line = Line(p1,p2)
            side = guide_line.get_center()
            normal_direction = guide_line.copy()
            normal_direction.rotate(PI/2)
            vector_normal_direction = normal_direction.get_unit_vector()
            direction = Dot(side).shift(vector_normal_direction*buff).get_center()
            coords_vertices.append(direction)

        return coords_vertices
    
    def get_center_of_edges_inside(self,buff=SMALL_BUFF*3):
        vertices = self.get_vertices()
        coords_vertices = []
        for i in range(len(vertices)):
            if i < len(vertices)-1:
                p1,p2 = [vertices[i],vertices[i+1]]
            else:
                p1,p2 = [vertices[-1],vertices[0]]
            guide_line = Line(p1,p2)
            side = guide_line.get_center()
            normal_direction = guide_line.copy()
            normal_direction.rotate(-PI/2)
            vector_normal_direction = normal_direction.get_unit_vector()
            direction = Dot(side).shift(vector_normal_direction*buff).get_center()
            coords_vertices.append(direction)

        return coords_vertices