import math
from manim import *

class Crankshaft(Scene):

    def construct(self):
        # Create Crankshaft BlackBox
        crankshaftBox = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        crankshaftText = Text("Crankshaft")
        crankshaftBlock = VGroup(crankshaftBox, crankshaftText)
        self.play(Create(crankshaftBox))
        self.play(FadeIn(crankshaftText))
        self.wait(0.5)

        crankshaftBlockInputText = Text("Torque").next_to(crankshaftBlock, LEFT * 5)
        crankshaftBlockInputArrow = Arrow(crankshaftBlockInputText.get_right(), crankshaftBox.get_left())
        self.play(FadeIn(crankshaftBlockInputText), run_time = 0.3)
        self.play(GrowArrow(crankshaftBlockInputArrow))
        self.wait()

        crankshaftBlockOutputText = Text("Rotation").next_to(crankshaftBlock, RIGHT * 5)
        crankshaftBlockOutputArrow = Arrow(crankshaftBox.get_right(),crankshaftBlockOutputText.get_left())
        self.play(GrowArrow(crankshaftBlockOutputArrow))
        self.play(FadeIn(crankshaftBlockOutputText), run_time = 0.3)
        self.wait()

        thetaText = MathTex("\\theta")
        thetaDotText = MathTex("\dot{\\theta}")
        thetaDotDotText = MathTex("\ddot{\\theta}")
        crankshaftOutputStateText = VGroup(thetaText, thetaDotText, thetaDotDotText).arrange(DOWN, center=False, aligned_edge=LEFT).move_to(crankshaftBlockOutputText.get_left())
        crankshaftBlockOutputArrow2 = Arrow(crankshaftBox.get_right(), crankshaftOutputStateText.get_left())
        self.play(ReplacementTransform(crankshaftBlockOutputText, crankshaftOutputStateText), ReplacementTransform(crankshaftBlockOutputArrow, crankshaftBlockOutputArrow2))
        self.wait()

        # Note the Crankshaft BlackBox
        crankshaftBlackBoxGroup = VGroup(crankshaftBlockInputText, crankshaftBlockInputArrow, crankshaftBlock, crankshaftBlockOutputArrow2, crankshaftOutputStateText)
        self.play(crankshaftBlackBoxGroup.animate.scale(0.5).to_corner(UL), run_time = 0.5)
        box1 = SurroundingRectangle(crankshaftBlackBoxGroup, buff = SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box1))
        crankshaftBlackBoxGroup.add(box1)
        self.wait()

        # Crankshaft Mathematical Model
        generalMathematicalModelTex = MathTex("I \\frac{d^{2}\\theta}{dt^{2}}", "+", "c \\frac{d\\theta}{dt}", "+", "k\\theta", "=", "T")
        self.play(Write(generalMathematicalModelTex))
        self.wait()
        for i in range(len(generalMathematicalModelTex)):
            if (i % 2) == 0:
                self.play(generalMathematicalModelTex[i].animate.set_color(YELLOW))
                self.wait()
                self.play(generalMathematicalModelTex[i].animate.set_color(WHITE))
        self.wait()
        mathematicalModelTex = MathTex("I \\frac{d^{2}\\theta}{dt^{2}}", "+", "c \\frac{d\\theta}{dt}", "=", "T")
        self.play(TransformMatchingTex(generalMathematicalModelTex,mathematicalModelTex))
        self.wait()

        # Note the Mathematical Model
        self.play(mathematicalModelTex.animate.scale(0.9).next_to(crankshaftBlackBoxGroup, RIGHT), run_time = 0.5)
        box2 = SurroundingRectangle(mathematicalModelTex, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box2))
        mathematicalModelGroup = VGroup(mathematicalModelTex, box2)
        self.wait()

        # Calculate Frequency
        frequecyCalculationTex = MathTex("Sampling\, Frequency", " \\geq ", "20000\, rpm", "\\cdot 2", "\\cdot 10")
        self.play(FadeIn(frequecyCalculationTex))
        self.play(frequecyCalculationTex[2].animate.set_color(YELLOW))
        self.wait()
        self.play(frequecyCalculationTex[2].animate.set_color(WHITE))
        frequecyCalculationTex2 = MathTex("Sampling\, Frequency", " \\geq ", "333\, rps", "\\cdot 2", "\\cdot 10")
        self.play(TransformMatchingTex(frequecyCalculationTex,frequecyCalculationTex2))
        self.wait()
        self.play(frequecyCalculationTex2[3].animate.set_color(YELLOW), frequecyCalculationTex2[4].animate.set_color(YELLOW))
        self.wait()
        self.play(FadeOut(frequecyCalculationTex2), run_time = 0.5)

        # Show Crank-Piston Cycle
        Xoffset = 2 * DOWN
        startAngle = PI/2
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

        rod.add_updater(
            lambda mob: mob.become(self.getline(self.getPointPos(l1, curAngle, startAngle, Xoffset),piston))
        )
        
        sampleLines = VGroup()
        j = 0

        for i in range(60):
            curAngle = (2 * PI) * (i / 60) + startAngle
            pistonPosition = math.sqrt(math.pow(l2,2) - math.pow(e + l1 * math.cos(curAngle),2)) + (l1 * math.sin(curAngle)) - d
            self.play(
                Rotate(crank, angle= 0.105),
                piston.animate.move_to(((pistonPosition * 5) + 1.5) * UP + Xoffset),
                run_time = 1/30)
            if i>29 :
                if((i%3) == 0):
                    sapmleLine = Line(pistonPosition * 5 * UP + 0.25 * RIGHT, pistonPosition * 5 * UP + 1.5 * LEFT).set_stroke(width=1) 
                    sampleText = Tex("sample").scale(0.4).next_to(sapmleLine, LEFT)
                    sample = VGroup(sapmleLine, sampleText)
                    sampleLines.add(sample)
                    self.add(sampleLines[j])
                    j = j + 1
        self.wait(2)

        self.play(FadeOut(rod), FadeOut(sampleLines), run_time = 0.2)
        self.play(FadeOut(crank), FadeOut(piston), run_time = 0.5)

        # Continue Calculate Frequency
        self.play(FadeIn(frequecyCalculationTex2))
        self.wait()
        frequecyCalculationTex3 = MathTex("Sampling\, Frequency", " \\geq ", "6660\, Hz")
        self.play(TransformMatchingShapes(frequecyCalculationTex2, frequecyCalculationTex3))
        self.wait()
        frequecyTex = MathTex("Frequency", "=", "10000\, Hz")
        self.play(TransformMatchingShapes(frequecyCalculationTex3, frequecyTex))
        self.wait()
        dtText = MathTex("Sample\, Time\, (dt)", "=", "0.0001\, s")
        fanddtTex = VGroup(frequecyTex, dtText).arrange(DOWN)
        self.play(TransformMatchingTex(frequecyTex, fanddtTex))
        self.wait()

        # Note the frequency and Sample Time
        self.play(fanddtTex.animate.scale(0.8).next_to(mathematicalModelGroup, RIGHT))
        box3 = SurroundingRectangle(fanddtTex, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box3))
        fanddtTexGroup = VGroup(fanddtTex, box3)
        self.wait()

        #chapter 1
        c1tex = Tex(r"Discrete\, Transfer\, Function", font_size=100)
        self.play(FadeIn(c1tex))
        self.wait()
        self.play(FadeOut(c1tex))
        self.wait()

        # Laplace
        laplaceRawTex = MathTex("I(s^{2}\\theta(s)-s\, \\theta(0)-{\\theta}'(0))", "+", "c(s\\theta(s)-\\theta(0))", "=", "T(s)")
        for i in range(len(laplaceRawTex)):
            self.play(TransformFromCopy(mathematicalModelTex[i], laplaceRawTex[i]))
        self.wait()

        laplace1 = MathTex("I(s^{2}\\theta(s)", "-s\, \\theta(0)-{\\theta}'(0)", ")", "+", "c(s\\theta(s)", "-\\theta(0)", ")", "=", "T(s)")
        laplace1[1].set_color(YELLOW)
        laplace1[5].set_color(YELLOW)
        self.play(FadeTransform(laplaceRawTex, laplace1))
        self.wait()
        laplace2 = MathTex("Is^{2}\\theta(s)", "+", "c\, s\\theta(s)", "=", "T(s)")
        self.play(FadeTransform(laplace1, laplace2))
        self.wait()
        laplace3 = MathTex("\\theta(s)(Is^{2}+ c\, s)=T(s)")
        self.play(TransformMatchingShapes(laplace2,laplace3))
        self.wait()
        transferFunction = MathTex("\\frac{\\theta(s)}{T(s)} = \\frac{1}{Is^{2}+ c\, s}")
        self.play(TransformMatchingShapes(laplace3,transferFunction))
        self.wait()

        # Note the TF
        self.play(transferFunction.animate.scale(0.85).next_to(crankshaftBlackBoxGroup, DOWN).to_edge(0.5 * LEFT), run_time = 0.5)
        box4 = SurroundingRectangle(transferFunction, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box4))
        self.wait()
        transferFunctionGroup = VGroup(transferFunction, box4)

        # Calculate Inertia and Damping
        Itext = Tex("I")
        cText = Tex("c")
        IandcText = VGroup(Itext, cText).arrange(RIGHT, buff=LARGE_BUFF).move_to(DOWN/2)
        self.play(FadeIn(IandcText))
        self.play(Itext.animate.move_to(3 * LEFT + DOWN/2), cText.animate.move_to(3.5 * RIGHT + DOWN/2))
        
        inertiaText = MathTex("(", "crankshaft", " + flywheel + 4 \\cdot piston + 4 \\cdot (piston + rod))\\cdot1.5").scale(0.6).next_to(Itext, 2 * DOWN)
        self.play(Write(inertiaText))
        self.wait()
        self.play(inertiaText[1].animate.set_color(YELLOW))
        inertiaCalculation = Text("From Fusion360 calculation, 0.04").scale(0.5).next_to(inertiaText, 2* DOWN)
        self.play(FadeIn(inertiaCalculation), run_time = 0.5)
        self.wait(0.5)

        inertiaText2 = MathTex("(0.04 + ", "flywheel", "+ 4 \\cdot (piston + rod))\\cdot1.5").scale(0.6).next_to(Itext, 2 * DOWN)
        self.play(TransformMatchingTex(inertiaText,inertiaText2), FadeOut(inertiaCalculation, shift=UP))
        self.play(inertiaText2[1].animate.set_color(YELLOW))
        inertiaCalculation2 = MathTex("(0.5)\\cdot7.15\\cdot0.12^{2}=0.0515").next_to(inertiaText2, 2* DOWN)
        self.play(FadeIn(inertiaCalculation2), run_time = 0.5)
        self.wait(0.5)

        inertiaText3 = MathTex("(0.04 + 0.0515 + 4 \\cdot (", "piston", "+ rod))\\cdot1.5").scale(0.6).next_to(Itext, 2 * DOWN)
        self.play(TransformMatchingTex(inertiaText2,inertiaText3), FadeOut(inertiaCalculation2, shift=UP))
        inertiaCalculation3 = MathTex("0.5 \\cdot 0.05^{2} = 0.00125").next_to(inertiaText3, 2* DOWN)
        self.play(inertiaText3[1].animate.set_color(YELLOW))
        self.play(FadeIn(inertiaCalculation3), run_time = 0.5)
        self.wait(0.5)

        inertiaText4 = MathTex("(0.04 + 0.0515 + 4 \\cdot (0.00125 + ", "rod", "))\\cdot1.5").scale(0.6).next_to(Itext, 2 * DOWN)
        self.play(TransformMatchingTex(inertiaText3,inertiaText4), FadeOut(inertiaCalculation3, shift=UP))
        inertiaCalculation4 = Text("From Fusion360 calculation, 0.0079").scale(0.5).next_to(inertiaText4, 2* DOWN)
        self.play(inertiaText4[1].animate.set_color(YELLOW))
        self.play(FadeIn(inertiaCalculation4), run_time = 0.5)
        self.wait(0.5)

        inertiaText5 = MathTex("(0.04 + 0.0515 + 4 \\cdot (0.00125 + 0.0079))\\cdot", "1.5").scale(0.6).next_to(Itext, 2 * DOWN)
        self.play(TransformMatchingTex(inertiaText4,inertiaText5), FadeOut(inertiaCalculation4, shift=UP))

        self.play(inertiaText5[1].animate.set_color(YELLOW))
        self.wait(0.5)
        self.play(inertiaText5[1].animate.set_color(WHITE))

        calculatedInertia = Text("Estimated Inertia = 0.19215").scale(0.5).next_to(inertiaText5, 2* DOWN)
        self.play(FadeIn(calculatedInertia))
        self.wait()

        frictionText = MathTex("(9\\cdot ", "Bearing Damping", "+ 4\\cdot Piston Damping)\\cdot1.5").scale(0.6).next_to(cText, 2 * DOWN)
        self.play(Write(frictionText))
        self.wait()
        self.play(frictionText[1].animate.set_color(YELLOW))
        self.wait()
        oilFriction = MathTex("T = \\frac{u \\cdot 4 \\cdot pi^{2} \\cdot r^{3} \\cdot L \\cdot \dot{\\theta}}{l \\cdot 57.2958}").scale(0.75).next_to(frictionText, 1.5*DOWN)
        self.play(Write(oilFriction))
        self.wait()
        oilFriction2 = MathTex("\\frac {T}{\dot{\\theta}} = \\frac{u \\cdot 4 \\cdot pi^{2} \\cdot r^{3} \\cdot L}{l \\cdot 57.2958}").scale(0.75).next_to(frictionText, 1.5*DOWN)
        self.play(TransformMatchingShapes(oilFriction, oilFriction2))
        self.wait()
        oilFriction3 = MathTex("\\frac {T}{\dot{\\theta}} = 0.0017").scale(0.75).next_to(frictionText, 1.5*DOWN)
        self.play(TransformMatchingShapes(oilFriction2, oilFriction3))
        self.wait()
        frictionText2 = MathTex("(9\\cdot 0.0017 + 4\\cdot ", "Piston Damping", ")\\cdot1.5").scale(0.6).next_to(cText, 2 * DOWN)
        self.play(TransformMatchingTex(frictionText, frictionText2), FadeOut(oilFriction3, shift=UP))
        self.play(frictionText2[1].animate.set_color(YELLOW))
        self.wait(0.5)
        oilFriction4 = MathTex("\\frac {T}{\dot{\\theta}} = 0.05").scale(0.75).next_to(frictionText2, 1.5*DOWN)
        self.play(Write(oilFriction4))
        self.wait()
        frictionText3 = MathTex("(9\\cdot 0.0017 + 4\\cdot 0.05)\\cdot", "1.5").scale(0.6).next_to(cText, 2 * DOWN)
        self.play(TransformMatchingTex(frictionText2, frictionText3), FadeOut(oilFriction4, shift=UP))

        self.play(Indicate(frictionText3[1]))

        calculatedDamping = Text("Estimated Damping = 0.32236").scale(0.5).next_to(frictionText3, 2* DOWN)
        self.play(FadeIn(calculatedDamping))
        self.wait()

        # Note the I and c

        finalITex = MathTex("I = 0.19215 \, kg/m^{2}").scale(0.75).move_to(Itext.get_center())
        finalcTex = MathTex("c = 0.32236 \, Nm / \\dot{\\theta}").scale(0.8).move_to(cText.get_center())

        self.play(TransformMatchingTex(Itext, finalITex),
                  TransformMatchingTex(cText, finalcTex))
        
        self.play(FadeOut(calculatedDamping),
                  FadeOut(inertiaText5),
                  FadeOut(calculatedInertia),
                  FadeOut(frictionText3))
        
        coeffsTex = VGroup(finalITex, finalcTex)
        
        self.play(coeffsTex.animate.arrange(DOWN, buff = SMALL_BUFF).next_to(transferFunctionGroup, RIGHT))
        self.wait()

        box5 = SurroundingRectangle(coeffsTex, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box5))
        self.wait()
        coeffsTexGroup = VGroup(coeffsTex, box5)

        # Explain MATLAB c2d
        continuesTimeText = Text("Continues Time").scale(0.85)
        discreateTimeText = Text("Discrete Time").scale(0.85)
        c2dText = VGroup(continuesTimeText, discreateTimeText).arrange(RIGHT, buff=3)
        c2dArrow = Arrow(c2dText[0].get_right(), c2dText[1].get_left())
        self.play(FadeIn(c2dText[0]))
        self.play(GrowArrow(c2dArrow),FadeIn(c2dText[1]), run_time = 0.5)
        self.wait()
        c2dText.add(c2dArrow)
        matlabc2dText = Tex("\(>\!\!>\)\, ", "sysd", " = ", "c2d(", "sysc", ", ", "Ts", ")")
        self.play(FadeTransform(c2dText, matlabc2dText))
        self.wait()
        self.play(matlabc2dText[1].animate.set_color(YELLOW))
        self.wait(1.5)
        self.play(matlabc2dText[1].animate.set_color(WHITE))
        self.play(matlabc2dText[4].animate.set_color(YELLOW))
        self.play(Circumscribe(transferFunction))
        self.wait()
        self.play(matlabc2dText[4].animate.set_color(WHITE))
        self.play(matlabc2dText[6].animate.set_color(YELLOW))
        self.play(Circumscribe(fanddtTex))
        self.wait()
        self.play(matlabc2dText[6].animate.set_color(WHITE))
        self.wait(0.5)
        self.play(FadeOut(matlabc2dText))

        # Create Discrete Model

        code = '''T = @(u, l, r, L) (u * 4 * pi^2 * r^3 * L / 57.2958) / l;
u = 0.02; % 70C SAE 30
l = 5.2e-5; %m
r = 0.05; %m
L = 0.05; %m
friction = ((T(u,l,r,L)) * 9 + 4 * 0.05) * 1.5;
inertia = (0.04 + 0.0515 + 0.00125 * 4 + 0.0079 * 4) * 1.5;
dt = 0.0001;
c2d(tf(1, [inertia friction 0]), dt)
'''
        rendered_code = Code(code=code, language="matlab", line_spacing=0.5, font="Monospace", stroke_width=1).scale(0.9).move_to(1.5 * DOWN)
        self.play(FadeIn(rendered_code))
        self.wait(2)
        result_code = '''ans =
 
  2.602e-08 z + 2.602e-08
  -----------------------
    z^2 - 2 z + 0.9998
 
Sample time: 0.0001 seconds
Discrete-time transfer function.
        '''
        rendered_result_code = Code(code=result_code, language="c", insert_line_no=False, line_spacing=0.5, font="Monospace", stroke_width=1).scale(0.9).move_to(1.5 * DOWN)
        self.play(ReplacementTransform(rendered_code, rendered_result_code))
        self.wait(2)

        # Note Discrete Model

        discreateTimeTransferFunction = MathTex("\\frac{\\theta(z)}{T(z)} = \\frac{2.602\, e-08\, z + 2.602\, e-08}{z^2 - 2\, z + 0.9998}").move_to(rendered_result_code.get_center())
        self.play(FadeOut(rendered_result_code), FadeIn(discreateTimeTransferFunction))
        self.wait()

        self.play(discreateTimeTransferFunction.animate.scale(0.85).next_to(coeffsTexGroup, RIGHT))
        box6 = SurroundingRectangle(discreateTimeTransferFunction, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box6))
        self.wait(2)
        discreateTimeTransferFunctionGroup = VGroup(discreateTimeTransferFunction, box6)

        # Z to Time Domain
        changeZpower = MathTex("\\frac{\\theta(z)}{T(z)} = \\frac{2.602\, e-08\, z + 2.602\, e-08}{z^2 - 2\, z + 0.9998}", "\\cdot \\frac{z^{-2}}{z^{-2}}")
        self.play(FadeIn(changeZpower[0]), Circumscribe(discreateTimeTransferFunction))
        self.wait()
        self.play(FadeIn(changeZpower[1]))
        self.wait(2)
        changeZpower2 = MathTex("\\frac{\\theta(z)}{T(z)} = \\frac{2.602\, e-08\, z^{-1} + 2.602\, e-08\, z^{-2}}{z - 2\, z^{-1} + 0.9998\, z^{-2}}")
        self.play(TransformMatchingShapes(changeZpower, changeZpower2))
        self.wait()
        makeEqFalt = MathTex("\\theta(z)z", "- 2\, ", "\\theta(z)z^{-1}", "+ 0.9998\, ", "\\theta(z)z^{-2}", " = 2.602\, e-08\, ", "T(z)z^{-1}", "+ 2.602\, e-08\, ", "T(z)z^{-2}").scale(0.75)
        self.play(TransformMatchingShapes(changeZpower2, makeEqFalt))
        self.wait()
        for i in range(len(makeEqFalt)):
            if (i % 2) == 0:
                self.play(makeEqFalt[i].animate.set_color(YELLOW), run_time = 0.5)
        self.wait()
        
        timeDomainEq = MathTex("\\theta(t)", "- 2\, ", "\\theta(t-dt)", "+ 0.9998\, ", "\\theta(t-2dt)", " = 2.602\, e-08\, ", "T(t-dt)", "+ 2.602\, e-08\, ", "T(t-2dt)").scale(0.75).next_to(makeEqFalt, DOWN)
        for i in range(len(timeDomainEq)):
            if (i % 2) == 0:
                timeDomainEq[i].set_color(YELLOW)

        for i in range(len(timeDomainEq)):
                self.play(TransformFromCopy(makeEqFalt[i], timeDomainEq[i]))
        self.wait()

        self.play(makeEqFalt.animate.set_color(WHITE))
        self.play(timeDomainEq.animate.set_color(WHITE))

        self.play(timeDomainEq[1].animate.set_color(YELLOW),
                  timeDomainEq[2].animate.set_color(YELLOW),
                  timeDomainEq[3].animate.set_color(YELLOW),
                  timeDomainEq[4].animate.set_color(YELLOW))
        
        self.wait()

        angleEquation = MathTex("\\theta(t)", "= 2\, ", "\\theta(t-dt)", "- 0.9998\, ", "\\theta(t-2dt)", " + 2.602\, e-08\, ", "T(t-dt)", "+ 2.602\, e-08\, ", "T(t-2dt)").scale(0.7).next_to(makeEqFalt, DOWN)
        self.play(TransformMatchingTex(timeDomainEq, angleEquation))
        self.wait()

        # Note the TimeDomainEq
        self.play(FadeOut(makeEqFalt), angleEquation.animate.next_to(transferFunctionGroup, DOWN).to_edge(LEFT))
        box7 = SurroundingRectangle(angleEquation, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box7))
        self.wait()
        angleEquationGroup = VGroup(angleEquation, box7)
        
        # Z domain Summary
        sbox1 = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        Text1 = Text("Black Box").move_to(sbox1.get_center())
        block1 = VGroup(sbox1, Text1)

        sbox2 = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        Text2 = Paragraph("Mathematical", "Model", alignment="center").scale(0.8).move_to(sbox2.get_center())
        block2 = VGroup(sbox2, Text2)
        
        sbox3 = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        Text3 = Paragraph("Sampling", "Frequency", alignment="center").scale(0.9).move_to(sbox3.get_center())
        block3 = VGroup(sbox3, Text3)

        sbox4 = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        Text4 = Paragraph("S-Domain", "(Laplace)", alignment="center").scale(0.9).move_to(sbox4.get_center())
        block4 = VGroup(sbox4, Text4)

        sbox5 = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        Text5 = Paragraph("Calculate", "Parameters", alignment="center").scale(0.9).move_to(sbox5.get_center())
        block5 = VGroup(sbox5, Text5)

        sbox6 = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        Text6 = Text("Z-Domain").scale(0.9).move_to(sbox6.get_center())
        block6 = VGroup(sbox6, Text6)

        sbox7 = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        Text7 = Paragraph("Time", "Domain", alignment="center").scale(0.9).move_to(sbox7.get_center())
        block7 = VGroup(sbox7, Text7)

        sbox8 = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        Text8 = Paragraph("Arrange", "Equations", alignment="center").scale(0.9).move_to(sbox8.get_center())
        block8 = VGroup(sbox8, Text8)

        blocksGroupTop = VGroup(block1, block2, block3, block4).arrange(RIGHT, buff= LARGE_BUFF * 1.5).scale(0.6).move_to(1 * DOWN + 0.25 * LEFT)
        blocksGroupBottom = VGroup(block8, block7, block6, block5).arrange(RIGHT, buff= LARGE_BUFF * 1.5).scale(0.6).next_to(blocksGroupTop, DOWN)
        
        for i in range(0,3):
             blocksGroupTop.add(Arrow(blocksGroupTop[i].get_right(), blocksGroupTop[i+1].get_left(), buff=SMALL_BUFF))
             blocksGroupBottom.add(Arrow(blocksGroupBottom[3-i].get_left(), blocksGroupBottom[2-i].get_right(), buff=SMALL_BUFF))

        curArrow = CurvedArrow(blocksGroupTop[3].get_right(), blocksGroupBottom[3].get_right(), angle = -PI/2)

        allNotes = VGroup(crankshaftBlackBoxGroup,
                          mathematicalModelGroup,
                          fanddtTexGroup,
                          transferFunctionGroup,
                          coeffsTexGroup,
                          discreateTimeTransferFunctionGroup,
                          angleEquationGroup)
        
        for i in range(0,4):
            self.play(FadeIn(blocksGroupTop[i]), run_time = 0.5)
            self.play(Circumscribe(allNotes[i], buff = 0))
            self.wait(0.3)
            if(i < 3):
                self.play(GrowArrow(blocksGroupTop[i + 4]), run_time = 0.3)
        
        self.play(FadeIn(curArrow), run_time = 0.25)

        for i in range(0,3):
            self.play(FadeIn(blocksGroupBottom[3 - i]), run_time = 0.5)
            self.play(Circumscribe(allNotes[i + 4], buff = 0))
            self.wait(0.3)
            self.play(GrowArrow(blocksGroupBottom[i + 4]), run_time = 0.3)

        self.play(FadeIn(blocksGroupBottom[0]))
        self.wait()

        self.play(FadeOut(blocksGroupBottom), FadeOut(curArrow), run_time = 0.5)
        self.play(FadeOut(blocksGroupTop), run_time = 0.5)

        # Rearrange Notes
        self.play(allNotes.animate.move_to(allNotes.get_center() + 0.75 * DOWN), run_time = 0.5)
        self.play(angleEquationGroup.animate.to_corner(UL), run_time = 0.5)
        self.play(angleEquationGroup[1].animate.set_stroke(color=RED, width=2), run_time = 0.25)
        self.wait(0.25)
        self.play(FadeOut(allNotes[3]), FadeOut(allNotes[5]), run_time = 0.5)
        self.play(allNotes[4].animate.next_to(allNotes[0], DOWN).to_edge(0.8 * LEFT), run_time = 0.5)

        #chapter 2
        c1tex = Tex(r"State\, Space\, Model", font_size=100).move_to(DOWN)
        self.play(FadeIn(c1tex))
        self.wait()
        self.play(FadeOut(c1tex))
        self.wait()

        # State Space
        stateSpaceTex = VGroup(MathTex("\dot{x}", "=", "A", "\\cdot",  "x",  "+", "B", "\\cdot", "u"), MathTex("y", "=", "C", "\\cdot", "x", "+", "D", "\\cdot", "u")).scale(1.1).arrange(DOWN, center=True).move_to(DOWN)
        self.play(Write(stateSpaceTex))
        self.wait()

        stateSpaceExplainTex =  VGroup(Tex("Derivative of State Vector"),
                                       Tex("System Matrix"),
                                       Tex("State Vector"),
                                       Tex("Input Matrix"),
                                       Tex("Input Vector"),
                                       Tex("Output Vector"),
                                       Tex("Output Matrix"),
                                       Tex("State Vector"),
                                       Tex("Feedforward Matrix"),
                                       Tex("Input Vector")).scale(1.25).set_color(YELLOW).next_to(stateSpaceTex, DOWN)

        e = 0
        for i in range(2):
            for j in range(len(stateSpaceTex[i])):
                if (j % 2) == 0:
                    self.play(stateSpaceTex[i][j].animate.set_color(YELLOW), FadeIn(stateSpaceExplainTex[e]), run_time = 0.5)
                    self.wait(0.75)
                    self.play(stateSpaceTex[i][j].animate.set_color(WHITE), FadeOut(stateSpaceExplainTex[e]), run_time = 0.5)
                    e += 1
        self.wait(0.5)

        # Note the state-space Eq
        self.play(stateSpaceTex.animate.scale(0.85).next_to(allNotes[4], RIGHT))
        box8 = SurroundingRectangle(stateSpaceTex, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box8))
        self.wait()
        stateSpaceTexGroup = VGroup(stateSpaceTex, box8)

        # Modelling States

        whatisStates = VGroup(MathTex(r"x = \begin{bmatrix} x_{1} \\ x_{2} \end{bmatrix}"), MathTex(r"\dot{x} = \begin{bmatrix} \dot{x}_{1} \\ \dot{x}_{2} \end{bmatrix}")).arrange(RIGHT).move_to(DOWN)
        self.play(FadeIn(whatisStates[0]))
        self.wait()
        self.play(FadeIn(whatisStates[1]))
        self.wait()

        self.play(whatisStates.animate.scale(0.85).next_to(stateSpaceTexGroup, RIGHT))
        box9 = SurroundingRectangle(whatisStates, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box9))
        self.wait()
        whatisStatesGroup = VGroup(whatisStates, box9)


        diffEquation = MathTex("I\, \\ddot{\\theta} + c\, \\dot{\\theta} = T").move_to(DOWN)
        generaldiffEquation = MathTex("I\, ", "\\ddot{\\theta}", "+ c\, ", "\\dot{\\theta}", "+ k\, ", "\\theta", "= T").move_to(DOWN)

        self.play(TransformFromCopy(mathematicalModelGroup[0],diffEquation))
        self.wait(2)
        self.play(TransformMatchingTex(diffEquation, generaldiffEquation))
        self.wait()

        self.play(generaldiffEquation[3].animate.set_color(YELLOW), generaldiffEquation[5].animate.set_color(YELLOW), run_time = 0.5)
        self.wait()
        self.play(generaldiffEquation[1].animate.set_color(YELLOW), generaldiffEquation[3].animate.set_color(WHITE), generaldiffEquation[5].animate.set_color(WHITE))
        self.wait(2)
        self.play(generaldiffEquation[1].animate.set_color(WHITE))
        self.wait()

        changeVariableRow1 = MathTex("x_{1}", "=\\theta")
        changeVariableRow2 = MathTex("x_{2}", "=\\dot{x}_{1}", "=\\dot{\\theta}")
        changeVariableRow3 = MathTex("\\dot{x}_{2}", "=\\ddot{x}_{1}", "=\\ddot{\\theta}")
        changeVariable = VGroup(changeVariableRow1,changeVariableRow2,changeVariableRow3).arrange(DOWN, center=False, aligned_edge=LEFT).next_to(generaldiffEquation, DOWN)

        self.play(FadeIn(changeVariable[0][0]), run_time = 0.5)
        self.wait(0.5)
        self.play(FadeIn(changeVariable[0][1]), run_time = 0.5)
        self.wait(0.5)
        for i in range(1,3):
            for j in range(3):
                self.play(FadeIn(changeVariable[i][j]), run_time = 0.5)
                self.wait(0.5)
        
        self.play(changeVariable.animate.scale(0.85).next_to(allNotes[2], 1.5 * DOWN).to_edge(RIGHT))
        box10 = SurroundingRectangle(changeVariable, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box10))
        self.wait()
        changeVariableGroup = VGroup(changeVariable, box10)

        # Diff Equation with new variables

        self.play(Circumscribe(stateSpaceTexGroup, buff = 0))
        self.wait(0.5)
        self.play(stateSpaceTexGroup[0][0].animate.set_color(YELLOW))
        self.wait()
        self.play(stateSpaceTexGroup[0][0].animate.set_color(WHITE), stateSpaceTexGroup[0][0][0].animate.set_color(YELLOW))
        self.wait()
        self.play(whatisStatesGroup[0][1].animate.set_color(YELLOW))
        self.wait(2)
        self.play(stateSpaceTexGroup[0].animate.set_color(WHITE), whatisStatesGroup[0].animate.set_color(WHITE))
        self.wait()

        # Get x_1_dot
        self.play(changeVariableGroup[0][1][0].animate.set_color(YELLOW),
                  changeVariableGroup[0][1][1].animate.set_color(YELLOW))
        self.wait(0.5)
        # keep x_1_dot
        getX1Dot = MathTex(r"\dot{x}_{1} = x_{2}").scale(0.75).next_to(allNotes[4], 1.5 * DOWN).to_edge(LEFT)
        self.play(TransformFromCopy(changeVariableGroup[0][1][1], getX1Dot), changeVariableGroup[0].animate.set_color(WHITE))
        self.wait(2)
        getX1DotClean = MathTex(r"\dot{x}_{1} = x_{2} + 0 \cdot x_{1} + 0 \cdot T").scale(0.75).next_to(allNotes[4], 1.5 * DOWN).to_edge(LEFT)
        self.play(FadeTransform(getX1Dot, getX1DotClean))
        self.wait(2)

        # Get x_2_dot
        self.play(generaldiffEquation[1].animate.set_color(YELLOW))
        self.wait()
        self.play(changeVariableGroup[0][2][0].animate.set_color(YELLOW), 
                  changeVariableGroup[0][2][2].animate.set_color(YELLOW))
        self.wait()
        generaldiffEquation2 = MathTex("I\, ", "\\dot{x}_{2}", "+ c\, ", "\\dot{\\theta}", "+ k\, ", "\\theta", "= T").move_to(DOWN) 
        self.play(TransformMatchingTex(generaldiffEquation, generaldiffEquation2), changeVariableGroup[0].animate.set_color(WHITE))
        self.wait(0.5)

        self.play(generaldiffEquation2[3].animate.set_color(YELLOW))
        self.wait(0.5)
        self.play(changeVariableGroup[0][1][0].animate.set_color(YELLOW), 
                  changeVariableGroup[0][1][2].animate.set_color(YELLOW))
        self.wait()
        generaldiffEquation3 = MathTex("I\, ", "\\dot{x}_{2}", "+ c\, ", "x_{2}", "+ k\, ", "\\theta", "= T").move_to(DOWN) 
        self.play(TransformMatchingTex(generaldiffEquation2, generaldiffEquation3), changeVariableGroup[0].animate.set_color(WHITE))
        self.wait(0.5)

        self.play(generaldiffEquation3[5].animate.set_color(YELLOW))
        self.wait(0.5)
        self.play(changeVariableGroup[0][0].animate.set_color(YELLOW))
        self.wait()
        generaldiffEquation4 = MathTex("I\, ", "\\dot{x}_{2}", "+ c\, ", "x_{2}", "+ k\, ", "x_{1}", "= T").move_to(DOWN) 
        self.play(TransformMatchingTex(generaldiffEquation3, generaldiffEquation4), changeVariableGroup[0].animate.set_color(WHITE))
        self.wait(0.5)

        getX2Dot = MathTex(r"I\, \dot{x}_{2} = - c\, x_{2} - k\, x_{1} + T").move_to(DOWN)
        self.play(TransformMatchingShapes(generaldiffEquation4, getX2Dot))
        self.wait()
        getX2DotClean = MathTex(r"\dot{x}_{2} = - \frac{c}{I}\, x_{2} - \frac{k}{I}\, x_{1} + \frac{1}{I}T").move_to(DOWN)
        self.play(TransformMatchingShapes(getX2Dot, getX2DotClean))
        self.wait()

        # keep x_2_dot
        self.play(getX2DotClean.animate.scale(0.75).next_to(getX1DotClean, DOWN).to_edge(LEFT))
        self.wait()
        
        # Note x1dot, x2dot
        x1dotx2dot = VGroup(getX1DotClean, getX2DotClean)
        box11 = SurroundingRectangle(x1dotx2dot, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box11))
        self.wait(2)
        x1dotx2dotGroup = VGroup(x1dotx2dot, box11)

        # Write Matrix Form        
        stateSpaceMatrix = MathTex(r"\begin{bmatrix} \dot{x}_{1} \\ \dot{x}_{2} \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -\frac{k}{I} & -\frac{c}{I} \end{bmatrix} \begin{bmatrix} x_{1} \\ x_{2} \end{bmatrix} + \begin{bmatrix} 0 \\ \frac{1}{I} \end{bmatrix} T").scale(0.88).next_to(x1dotx2dotGroup, RIGHT)
        self.play(Write(stateSpaceMatrix), Circumscribe(x1dotx2dotGroup, buff = 0))
        self.wait(2)
        stateSpaceMatrixClean = MathTex(r"\begin{bmatrix} \dot{\theta} \\ \ddot{\theta} \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -\frac{k}{I} & -\frac{c}{I} \end{bmatrix} \begin{bmatrix} \theta \\ \dot{\theta} \end{bmatrix} + \begin{bmatrix} 0 \\ \frac{1}{I} \end{bmatrix} T").scale(0.88).next_to(x1dotx2dotGroup, RIGHT)
        self.play(TransformMatchingTex(stateSpaceMatrix, stateSpaceMatrixClean))
        self.wait()
        box12 = SurroundingRectangle(stateSpaceMatrixClean, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        self.play(Create(box12))
        self.wait()
        stateSpaceMatrixGroup = VGroup(stateSpaceMatrixClean, box12)

        # Delete unnecessary notes
        self.play(FadeOut(changeVariableGroup), FadeOut(whatisStatesGroup),FadeOut(x1dotx2dotGroup))
        self.wait(1)
        self.play(stateSpaceMatrixGroup.animate.next_to(stateSpaceTexGroup, RIGHT))
        self.wait()

        # y
        self.play(stateSpaceTexGroup[0][1].animate.set_color(YELLOW))
        self.play(stateSpaceTexGroup[0][1].animate.set_color(WHITE))
        self.wait(0.5)
        yeq = MathTex(r"\theta = \begin{bmatrix} 1 \ 0 \end{bmatrix} \begin{bmatrix} \theta \\ \dot{\theta} \end{bmatrix} + 0 \cdot T").move_to(DOWN)
        self.play(Write(yeq))
        self.wait(2)
        self.play(FadeOut(yeq))
        
        # State Space Summary
        stateSpaceMatrixClean = MathTex(r"\begin{bmatrix} \dot{\theta} \\ \ddot{\theta} \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -\frac{k}{I} & -\frac{c}{I} \end{bmatrix} \begin{bmatrix} \theta \\ \dot{\theta} \end{bmatrix} + \begin{bmatrix} 0 \\ \frac{1}{I} \end{bmatrix} T").scale(0.88).next_to(x1dotx2dotGroup, RIGHT)

        stateSpaceA = MathTex(r"A = \begin{bmatrix} 0 & 1 \\ -\frac{k}{I} & -\frac{c}{I} \end{bmatrix}")
        stateSpaceB = MathTex(r"B = \begin{bmatrix} 0 \\ \frac{1}{I} \end{bmatrix}")
        stateSpaceC = MathTex(r"C = \begin{bmatrix} 1 \ 0 \end{bmatrix}")
        stateSpaceD = MathTex(r"D = 0")

        ABGroup = VGroup(stateSpaceA,stateSpaceB).arrange(RIGHT)
        CDGroup = VGroup(stateSpaceC,stateSpaceD).arrange(DOWN).scale(0.85)
        ABCD = VGroup(ABGroup, CDGroup).arrange(RIGHT).scale(0.8).next_to(stateSpaceTexGroup, RIGHT)
        box13 = SurroundingRectangle(ABCD, buff=SMALL_BUFF).set_stroke(color=GREEN, width=1)
        ABCDGruop = VGroup(ABCD, box13)
        self.play(ReplacementTransform(stateSpaceMatrixGroup, ABCDGruop))
        self.wait()

        ssbox1 = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        ssText1 = Text("Black Box").move_to(ssbox1.get_center())
        ssblock1 = VGroup(ssbox1, ssText1)

        ssbox2 = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        ssText2 = Paragraph("Mathematical", "Model", alignment="center").scale(0.8).move_to(ssbox2.get_center())
        ssblock2 = VGroup(ssbox2, ssText2)
        
        ssbox3 = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        ssText3 = Paragraph("State", "Space", alignment="center").scale(0.9).move_to(ssbox3.get_center())
        ssblock3 = VGroup(ssbox3, ssText3)

        ssbox4 = Rectangle(width=4, height=2).set_stroke(color=WHITE, width=2)
        ssText4 = Paragraph("Calculate", "Parameters", alignment="center").scale(0.9).move_to(ssbox4.get_center())
        ssblock4 = VGroup(ssbox4, ssText4)

        ssblocksGroup = VGroup(ssblock1, ssblock2, ssblock3, ssblock4).arrange(RIGHT, buff= LARGE_BUFF * 1.5).scale(0.6).move_to(1 * DOWN)
        
        for i in range(0,3):
             ssblocksGroup.add(Arrow(ssblocksGroup[i].get_right(), ssblocksGroup[i+1].get_left(), buff=SMALL_BUFF))

        ssNotes = VGroup(crankshaftBlackBoxGroup,
                         mathematicalModelGroup,
                         VGroup(stateSpaceTexGroup,ABCDGruop),
                         VGroup(fanddtTexGroup,coeffsTexGroup))
        
        for i in range(0,4):
            self.play(FadeIn(ssblocksGroup[i]))
            if(i > 2):
                self.play(Circumscribe(ssNotes[i][0], buff = 0), Circumscribe(ssNotes[i][1], buff = 0))
            else:
                self.play(Circumscribe(ssNotes[i], buff = 0))
            self.wait(0.5)
            if(i < 3):
                self.play(GrowArrow(ssblocksGroup[i + 4]), run_time = 0.25)

        self.play(FadeOut(ssblocksGroup), run_time = 0.5)
        self.wait()

        # Final Notes
        self.play(FadeOut(crankshaftBlackBoxGroup),
                  FadeOut(mathematicalModelGroup),
                  FadeOut(fanddtTexGroup))
        
        finalSSNotes = VGroup(coeffsTexGroup, stateSpaceTexGroup, ABCDGruop)
        self.play(finalSSNotes.animate.scale(0.98).move_to(finalSSNotes.get_center() + 1.4 * UP))
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