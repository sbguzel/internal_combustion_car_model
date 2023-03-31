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
        rod = self.getline(0*UP + 0*DOWN + Xoffset,piston)

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
        
        zero = MathTex("0^{\\circ}", stroke_width = 2).scale(0.8).set_color(RED).next_to(yLine, UP)
        origin = MathTex("(0,0)", stroke_width = 2).scale(0.8).set_color(RED).next_to(crank.get_center(), DOWN * 0.5)

        self.play(Create(xLine), Create(yLine))
        self.wait()
        self.play(FadeIn(zero), FadeIn(origin))

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
            lambda mob: mob.become(self.getline(self.getPointPos(l1, curAngle, startAngle, Xoffset),piston))
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

        crankpistonmodel = VGroup(rod, crank, piston)

        point1 = Dot(point = 2 * DOWN, radius = 0.08)
        point2 = Dot(point = self.getPointPos(l1, curAngle, startAngle, Xoffset), radius = 0.08)
        point3 = Dot(point = piston.get_top(), radius = 0.08)

        line_1 = Line(point1.get_center(), point2.get_center()).set_stroke(width=5)
        line_2 = Line(point2.get_center(), point3.get_center()).set_stroke(width=5)

        self.play(FadeIn(point1, point2, point3, line_1, line_2), FadeOut(crankpistonmodel))

        self.wait()

        # Focus
        yText.clear_updaters()
        eline.clear_updaters()
        etext.clear_updaters()
        pistonTipLine.clear_updaters()
        showAngleLineText.clear_updaters()

        self.play(eline.animate.become(Line(2 * DOWN + e * 5 * RIGHT, point3.get_center()).set_stroke(width=1).set_opacity(0.75)),
                  pistonTipLine.animate.become(Line(point3.get_center(), point3.get_center() + e * 5 * LEFT)).set_stroke(width=1).set_opacity(0.75))
        
        thetaAngle = Angle(line_1, yLine, other_angle=True, radius=0.4).set_stroke(width=1).set_opacity(0.75)

        self.play(FadeOut(pistonTipArrow, earrow1, earrow2, showAngle, showAngleLine),
                  FadeIn(thetaAngle))
        
        self.play(etext.animate.next_to(pistonTipLine, UP),
                  yText.animate.next_to(eline, 0.5 * RIGHT),
                  showAngleLineText.animate.become(MathTex("\\theta").scale(0.75).set_color(WHITE).next_to(thetaAngle, 0.1 * UP)))
                
        self.wait()
        
        



    def getline(self, Point1, Point2):
        start_point = Point1
        end_point = Point2.get_center()
        line = Line(start_point,end_point).set_stroke(width=50).set_opacity(0.75)
        return line

    def getPointPos(self, l1, curAngle, startAngle, Xoffset):
            curAngle += PI/30
            crankXpos = (l1 * 5) * math.cos(curAngle - startAngle)
            crankYpos = -(l1 * 5) * math.sin(curAngle - startAngle)
            return crankXpos * UP + crankYpos * RIGHT + Xoffset


