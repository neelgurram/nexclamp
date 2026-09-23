'''
Neuron simulator export for:

Components:
    null (Type: notes)
    Ca_HVA (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Ca_LVAst (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Ih (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Im (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    K_Pst (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    K_Tst (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    KdShu2007 (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    Nap_Et2 (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    NaTa_t (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    NaTs2_t (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    SK_E2 (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    SKv3_1 (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    CaDynamics_E2_NML2 (Type: concentrationModelHayEtAl:  gamma=0.05 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.08 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cSTUT_7_axonal (Type: concentrationModelHayEtAl:  gamma=0.010353 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.06427799000000001 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cSTUT_7_somatic (Type: concentrationModelHayEtAl:  gamma=5.11E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.731707637 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__dNAC_1_axonal (Type: concentrationModelHayEtAl:  gamma=0.010353 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.06427799000000001 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__dNAC_1_somatic (Type: concentrationModelHayEtAl:  gamma=5.11E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.731707637 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__bNAC_1_axonal (Type: concentrationModelHayEtAl:  gamma=0.001739 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.468069681 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__bNAC_1_somatic (Type: concentrationModelHayEtAl:  gamma=5.0E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.645079741 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__bSTUT_1_axonal (Type: concentrationModelHayEtAl:  gamma=0.001739 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.468069681 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__bSTUT_1_somatic (Type: concentrationModelHayEtAl:  gamma=5.0E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.645079741 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cADpyr_229_axonal (Type: concentrationModelHayEtAl:  gamma=0.016713 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.384114655 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cADpyr_229_somatic (Type: concentrationModelHayEtAl:  gamma=5.33E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.342544232 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cADpyr_230_axonal (Type: concentrationModelHayEtAl:  gamma=5.02E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.179044149 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cADpyr_230_somatic (Type: concentrationModelHayEtAl:  gamma=0.002253 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.7394164970000001 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cADpyr_231_axonal (Type: concentrationModelHayEtAl:  gamma=0.001734 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.10309139 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cADpyr_231_somatic (Type: concentrationModelHayEtAl:  gamma=9.96E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.873498863 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cNAC_149_axonal (Type: concentrationModelHayEtAl:  gamma=0.010353 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.06427799000000001 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cNAC_149_somatic (Type: concentrationModelHayEtAl:  gamma=5.11E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.731707637 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cIR_1_axonal (Type: concentrationModelHayEtAl:  gamma=5.03E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.573007045 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cIR_1_somatic (Type: concentrationModelHayEtAl:  gamma=8.14E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.967678789 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__bIR_1_axonal (Type: concentrationModelHayEtAl:  gamma=0.003923 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.020715642 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__bIR_1_somatic (Type: concentrationModelHayEtAl:  gamma=8.93E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.605033222 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__bAC_1_axonal (Type: concentrationModelHayEtAl:  gamma=0.003923 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.020715642 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__bAC_1_somatic (Type: concentrationModelHayEtAl:  gamma=8.93E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.605033222 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cACint_237_axonal (Type: concentrationModelHayEtAl:  gamma=5.03E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.573007045 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cACint_237_somatic (Type: concentrationModelHayEtAl:  gamma=8.14E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.967678789 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__dSTUT_1_axonal (Type: concentrationModelHayEtAl:  gamma=0.010353 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.06427799000000001 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__dSTUT_1_somatic (Type: concentrationModelHayEtAl:  gamma=5.11E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.731707637 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cADpyr_232_axonal (Type: concentrationModelHayEtAl:  gamma=0.00291 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.28719873100000004 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    CaDynamics_E2_NML2__cADpyr_232_somatic (Type: concentrationModelHayEtAl:  gamma=6.09E-4 (dimensionless) minCai=1.0E-4 (SI concentration) decay=0.21048528400000002 (SI time) depth=1.0E-7 (SI length) Faraday=96485.3 (SI charge_per_mole) AREA_SCALE=1.0 (SI area) LENGTH_SCALE=1.0 (SI length))
    null (Type: notes)
    pas (Type: ionChannelPassive:  conductance=1.0E-11 (SI conductance))
    Soma_AllNML2 (Type: cell)
    null (Type: notes)
    Ca (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    Input_4 (Type: pulseGenerator:  delay=0.3 (SI time) duration=0.1 (SI time) amplitude=5.0E-11 (SI current))
    Input_3 (Type: pulseGenerator:  delay=0.1 (SI time) duration=0.1 (SI time) amplitude=-1.0000000000000001E-11 (SI current))
    network_Soma_AllNML2 (Type: networkWithTemperature:  temperature=279.45 (SI temperature))
    sim1 (Type: Simulation:  length=0.6 (SI time) step=1.0E-6 (SI time))


    This NEURON file has been generated by org.neuroml.export (see https://github.com/NeuroML/org.neuroml.export)
         org.neuroml.export  v1.11.0
         org.neuroml.model   v1.11.0
         jLEMS               v0.12.0

'''

import neuron

import time
import datetime
import sys

import hashlib
h = neuron.h
h.load_file("nrngui.hoc")

h("objref p")
h("p = new PythonObject()")

class NeuronSimulation():

    def __init__(self, tstop, dt=None, seed=123456789, abs_tol=None, rel_tol=None):

        print("\n    Starting simulation in NEURON of %sms generated from NeuroML2 model...\n"%tstop)

        self.setup_start = time.time()
        self.seed = seed
        self.abs_tol = abs_tol
        self.rel_tol = rel_tol
        import socket
        self.report_file = open('simulator.props','w')
        print('Simulator version:  %s'%h.nrnversion())
        self.report_file.write('# Report of running simulation with %s\n'%h.nrnversion())
        self.report_file.write('Simulator=NEURON\n')
        self.report_file.write('SimulatorVersion=%s\n'%h.nrnversion())

        self.report_file.write('SimulationFile=%s\n'%__file__)
        self.report_file.write('PythonVersion=%s\n'%sys.version.replace('\n',' '))
        print('Python version:     %s'%sys.version.replace('\n',' '))
        self.report_file.write('NeuroMLExportVersion=1.11.0\n')
        self.report_file.write('SimulationSeed=%s\n'%self.seed)
        self.report_file.write('Hostname=%s\n'%socket.gethostname())
        self.randoms = []
        self.next_global_id = 0  # Used in Random123 classes for elements using random(), etc. 

        self.next_spiking_input_id = 0  # Used in Random123 classes for elements using random(), etc. 

        '''
        Adding simulation Component(id=sim1 type=Simulation) of network/component: network_Soma_AllNML2 (Type: networkWithTemperature:  temperature=279.45 (SI temperature))
        
        '''

        # Temperature used for network: 279.45 K
        h.celsius = 279.45 - 273.15

        # ######################   Population: CG_TestCML
        print("Population CG_TestCML contains 1 instance(s) of component: Soma_AllNML2 of type: cell")

        print("Setting the default initial concentrations for ca (used in Soma_AllNML2) to 5.0E-5 mM (internal), 2.0 mM (external)")
        h("cai0_ca_ion = 5.0E-5")
        h("cao0_ca_ion = 2.0")

        h.load_file("Soma_AllNML2.hoc")
        a_CG_TestCML = []
        h("{ n_CG_TestCML = 1 }")
        h("objectvar a_CG_TestCML[n_CG_TestCML]")
        for i in range(int(h.n_CG_TestCML)):
            h("a_CG_TestCML[%i] = new Soma_AllNML2()"%i)
            h("access a_CG_TestCML[%i].Soma"%i)

            self.next_global_id+=1

        h("{ a_CG_TestCML[0].position(105.841934, 19.6415, 55.338722) }")

        h("proc initialiseV_CG_TestCML() { for i = 0, n_CG_TestCML-1 { a_CG_TestCML[i].set_initial_v() } }")
        h("objref fih_CG_TestCML")
        h('{fih_CG_TestCML = new FInitializeHandler(0, "initialiseV_CG_TestCML()")}')

        h("proc initialiseIons_CG_TestCML() { for i = 0, n_CG_TestCML-1 { a_CG_TestCML[i].set_initial_ion_properties() } }")
        h("objref fih_ion_CG_TestCML")
        h('{fih_ion_CG_TestCML = new FInitializeHandler(1, "initialiseIons_CG_TestCML()")}')

        print("Processing 2 input lists")

        # ######################   Input List: Input_4
        # Adding single input: Component(id=0 type=input)
        h("objref Input_4_0")
        h("a_CG_TestCML[0].Soma { Input_4_0 = new Input_4(0.5) } ")

        # ######################   Input List: Input_3
        # Adding single input: Component(id=0 type=input)
        h("objref Input_3_0")
        h("a_CG_TestCML[0].Soma { Input_3_0 = new Input_3(0.5) } ")

        print("Finished processing 2 input lists")

        trec = h.Vector()
        trec.record(h._ref_t)

        h.tstop = tstop

        if self.abs_tol is not None and self.rel_tol is not None:
            cvode = h.CVode()
            cvode.active(1)
            cvode.atol(self.abs_tol)
            cvode.rtol(self.rel_tol)
        else:
            h.dt = dt
            h.steps_per_ms = 1/h.dt

        # ######################   Display: self.display_CG_TestMod_v
        self.display_CG_TestMod_v = h.Graph(0)
        self.display_CG_TestMod_v.size(0,h.tstop,-80.0,50.0)
        self.display_CG_TestMod_v.view(0, -80.0, h.tstop, 130.0, 80, 330, 330, 250)
        h.graphList[0].append(self.display_CG_TestMod_v)
        # Line, plotting: CG_TestCML/0/Soma_AllNML2/v
        self.display_CG_TestMod_v.addexpr("a_CG_TestCML[0].Soma.v(0.5)", "a_CG_TestCML[0].Soma.v(0.5)", 1, 1, 0.8, 0.9, 2)

        # ######################   Display: self.display_GraphWin_5
        self.display_GraphWin_5 = h.Graph(0)
        self.display_GraphWin_5.size(0,h.tstop,-80.0,50.0)
        self.display_GraphWin_5.view(0, -80.0, h.tstop, 130.0, 80, 330, 330, 250)
        h.graphList[0].append(self.display_GraphWin_5)
        # Line, plotting: CG_TestCML/0/Soma_AllNML2/caConc
        self.display_GraphWin_5.addexpr("a_CG_TestCML[0].Soma.cai(0.5)", "a_CG_TestCML[0].Soma.cai(0.5)", 1, 1, 0.8, 0.9, 2)

        # ######################   Display: self.display_GraphWin_4
        self.display_GraphWin_4 = h.Graph(0)
        self.display_GraphWin_4.size(0,h.tstop,-80.0,50.0)
        self.display_GraphWin_4.view(0, -80.0, h.tstop, 130.0, 80, 330, 330, 250)
        h.graphList[0].append(self.display_GraphWin_4)
        # Line, plotting: CG_TestCML/0/Soma_AllNML2/biophys/membraneProperties/Ca_HVA_all/erev
        self.display_GraphWin_4.addexpr("a_CG_TestCML[0].Soma.erev(0.5)", "a_CG_TestCML[0].Soma.erev(0.5)", 1, 1, 0.8, 0.9, 2)

        # ######################   Display: self.display_GraphWin_0
        self.display_GraphWin_0 = h.Graph(0)
        self.display_GraphWin_0.size(0,h.tstop,-80.0,50.0)
        self.display_GraphWin_0.view(0, -80.0, h.tstop, 130.0, 80, 330, 330, 250)
        h.graphList[0].append(self.display_GraphWin_0)
        # Line, plotting: CG_TestCML/0/Soma_AllNML2/biophys/membraneProperties/Ih_all/Ih/m/q
        self.display_GraphWin_0.addexpr("a_CG_TestCML[0].Soma.m_q_Ih(0.5)", "a_CG_TestCML[0].Soma.m_q_Ih(0.5)", 1, 1, 0.8, 0.9, 2)
        # Line, plotting: CG_TestCML/0/Soma_AllNML2/biophys/membraneProperties/Im_all/Im/m/q
        self.display_GraphWin_0.addexpr("a_CG_TestCML[0].Soma.m_q_Im(0.5)", "a_CG_TestCML[0].Soma.m_q_Im(0.5)", 2, 1, 0.8, 0.9, 2)
        # Line, plotting: CG_TestCML/0/Soma_AllNML2/biophys/membraneProperties/KdShu2007_all/KdShu2007/m/q
        self.display_GraphWin_0.addexpr("a_CG_TestCML[0].Soma.m_q_KdShu2007(0.5)", "a_CG_TestCML[0].Soma.m_q_KdShu2007(0.5)", 3, 1, 0.8, 0.9, 2)
        # Line, plotting: CG_TestCML/0/Soma_AllNML2/biophys/membraneProperties/KdShu2007_all/KdShu2007/h/q
        self.display_GraphWin_0.addexpr("a_CG_TestCML[0].Soma.h_q_KdShu2007(0.5)", "a_CG_TestCML[0].Soma.h_q_KdShu2007(0.5)", 4, 1, 0.8, 0.9, 2)
        # Line, plotting: CG_TestCML/0/Soma_AllNML2/biophys/membraneProperties/Ca_HVA_all/Ca_HVA/m/q
        self.display_GraphWin_0.addexpr("a_CG_TestCML[0].Soma.m_q_Ca_HVA(0.5)", "a_CG_TestCML[0].Soma.m_q_Ca_HVA(0.5)", 5, 1, 0.8, 0.9, 2)
        # Line, plotting: CG_TestCML/0/Soma_AllNML2/biophys/membraneProperties/Ca_HVA_all/Ca_HVA/h/q
        self.display_GraphWin_0.addexpr("a_CG_TestCML[0].Soma.h_q_Ca_HVA(0.5)", "a_CG_TestCML[0].Soma.h_q_Ca_HVA(0.5)", 6, 1, 0.8, 0.9, 2)



        # ######################   File to save: CG_TestCML_0.CaDynamics_E2_NML2_CONC_ca.dat (Var_35_OF)
        # Column: CG_TestCML/0/Soma_AllNML2/caConc
        h(' objectvar v_caConc_Var_35_OF ')
        h(' { v_caConc_Var_35_OF = new Vector() } ')
        h(' { v_caConc_Var_35_OF.record(&a_CG_TestCML[0].Soma.cai(0.5)) } ')
        if self.abs_tol is None or self.rel_tol is None:

            h.v_caConc_Var_35_OF.resize((h.tstop * h.steps_per_ms) + 1)

        # ######################   File to save: time.dat (time)
        # Column: time
        h(' objectvar v_time ')
        h(' { v_time = new Vector() } ')
        h(' { v_time.record(&t) } ')
        if self.abs_tol is None or self.rel_tol is None:

            h.v_time.resize((h.tstop * h.steps_per_ms) + 1)

        # ######################   File to save: CG_TestCML_0.dat (CG_TestCML_v_OF)
        # Column: CG_TestCML/0/Soma_AllNML2/v
        h(' objectvar v_v_CG_TestCML_v_OF ')
        h(' { v_v_CG_TestCML_v_OF = new Vector() } ')
        h(' { v_v_CG_TestCML_v_OF.record(&a_CG_TestCML[0].Soma.v(0.5)) } ')
        if self.abs_tol is None or self.rel_tol is None:

            h.v_v_CG_TestCML_v_OF.resize((h.tstop * h.steps_per_ms) + 1)

        self.initialized = False

        self.sim_end = -1 # will be overwritten

        setup_end = time.time()
        self.setup_time = setup_end - self.setup_start
        print("Setting up the network to simulate took %f seconds"%(self.setup_time))

        h.nrncontrolmenu()


    def run(self):

        self.initialized = True
        sim_start = time.time()
        if self.abs_tol is not None and self.rel_tol is not None:
            print("Running a simulation of %sms (cvode abs_tol = %sms, rel_tol = %sms; seed=%s)" % (h.tstop, self.abs_tol, self.rel_tol, self.seed))
        else:
            print("Running a simulation of %sms (dt = %sms; seed=%s)" % (h.tstop, h.dt, self.seed))

        try:
            h.run()
        except Exception as e:
            print("Exception running NEURON: %s" % (e))
            return


        self.sim_end = time.time()
        self.sim_time = self.sim_end - sim_start
        print("Finished NEURON simulation in %f seconds (%f mins)..."%(self.sim_time, self.sim_time/60.0))

        try:
            self.save_results()
        except Exception as e:
            print("Exception saving results of NEURON simulation: %s" % (e))
            return


    def advance(self):

        if not self.initialized:
            h.finitialize()
            self.initialized = True

        h.fadvance()


    ###############################################################################
    # Hash function to use in generation of random value
    # This is copied from NetPyNE: https://github.com/Neurosim-lab/netpyne/blob/master/netpyne/simFuncs.py
    ###############################################################################
    def _id32 (self,obj): 
        return int(hashlib.md5(obj.encode('utf-8')).hexdigest()[0:8],16)  # convert 8 first chars of md5 hash in base 16 to int


    ###############################################################################
    # Initialize the stim randomizer
    # This is copied from NetPyNE: https://github.com/Neurosim-lab/netpyne/blob/master/netpyne/simFuncs.py
    ###############################################################################
    def _init_stim_randomizer(self,rand, stimType, gid, seed): 
        #print("INIT STIM  %s; %s; %s; %s"%(rand, stimType, gid, seed))
        rand.Random123(self._id32(stimType), gid, seed)


    def save_results(self):

        print("Saving results at t=%s..."%h.t)

        if self.sim_end < 0: self.sim_end = time.time()

        self.display_CG_TestMod_v.exec_menu("View = plot")
        self.display_GraphWin_5.exec_menu("View = plot")
        self.display_GraphWin_4.exec_menu("View = plot")
        self.display_GraphWin_0.exec_menu("View = plot")

        # ######################   File to save: time.dat (time). Note, saving in SI units
        py_v_time = [ t/1000 for t in h.v_time.to_python() ]  # Convert to Python list for speed...

        f_time_f2 = open('time.dat', 'w')
        num_points = len(py_v_time)  # Simulation may have been stopped before tstop...

        for i in range(num_points):
            f_time_f2.write('%f'% py_v_time[i])  # Save in SI units...
        f_time_f2.close()
        print("Saved data to: time.dat")

        # ######################   File to save: CG_TestCML_0.CaDynamics_E2_NML2_CONC_ca.dat (Var_35_OF). Note, saving in SI units
        py_v_caConc_Var_35_OF = [ float(x ) for x in h.v_caConc_Var_35_OF.to_python() ]  # Convert to Python list for speed, variable has dim: concentration

        f_Var_35_OF_f2 = open('CG_TestCML_0.CaDynamics_E2_NML2_CONC_ca.dat', 'w')
        num_points = len(py_v_time)  # Simulation may have been stopped before tstop...

        for i in range(num_points):
            f_Var_35_OF_f2.write('%e\t%e\t\n' % (py_v_time[i], py_v_caConc_Var_35_OF[i], ))
        f_Var_35_OF_f2.close()
        print("Saved data to: CG_TestCML_0.CaDynamics_E2_NML2_CONC_ca.dat")

        # ######################   File to save: CG_TestCML_0.dat (CG_TestCML_v_OF). Note, saving in SI units
        py_v_v_CG_TestCML_v_OF = [ float(x  / 1000.0) for x in h.v_v_CG_TestCML_v_OF.to_python() ]  # Convert to Python list for speed, variable has dim: voltage

        f_CG_TestCML_v_OF_f2 = open('CG_TestCML_0.dat', 'w')
        num_points = len(py_v_time)  # Simulation may have been stopped before tstop...

        for i in range(num_points):
            f_CG_TestCML_v_OF_f2.write('%e\t%e\t\n' % (py_v_time[i], py_v_v_CG_TestCML_v_OF[i], ))
        f_CG_TestCML_v_OF_f2.close()
        print("Saved data to: CG_TestCML_0.dat")

        save_end = time.time()
        save_time = save_end - self.sim_end
        print("Finished saving results in %f seconds"%(save_time))

        self.report_file.write('StartTime=%s\n'%datetime.datetime.fromtimestamp(self.setup_start).strftime('%Y-%m-%d %H:%M:%S'))
        self.report_file.write('SetupTime=%s\n'%self.setup_time)
        self.report_file.write('RealSimulationTime=%s\n'%self.sim_time)
        self.report_file.write('SimulationSaveTime=%s\n'%save_time)
        self.report_file.close()

        print("Saving report of simulation to %s"%('simulator.props'))

        print("Done")

if __name__ == '__main__':

    ns = NeuronSimulation(tstop=600.0, dt=0.001, seed=123456789, abs_tol=None, rel_tol=None)

    ns.run()

