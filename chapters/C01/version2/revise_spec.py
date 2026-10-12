from pathlib import Path
import json,copy
HERE=Path(__file__).resolve().parent
s=json.loads((HERE.parent/'lecture.json').read_text());s['version']=2;s['output_filename']='From_Brain_to_Behavior_Foundations_and_Frontiers_V2.pptx'
BOOK='Carlson NR, Birkett MA (2022). Physiology of Behavior, Global Edition, 13th edition. Pearson. ISBN 9781292430256. Introduction, pp. 15–34; brief cellular prerequisites from Structure and Functions of Cells of the Nervous System, pp. 35–69.'
rows={
6:('Brain activity can be measured through its blood supply',[
'Active brain tissue needs oxygen and nutrients. Local blood flow changes with neural activity. **Functional magnetic resonance imaging**, or fMRI, detects a signal related to blood oxygenation, allowing researchers to compare activity across brain regions.',
'**Functional connectivity** means that the activity signals from two regions change together over time. Imagine comparing two changing recordings: similar rises and falls indicate coordinated fluctuations. A network is a collection of regions with organized relationships among these signals.',
'The map identifies visual, movement-related, and attention-related networks in the cortex. These categories describe systems that cooperate during behavior. Comparing their signals helps connect the textbook idea of organized brain function with a measurable pattern.']),
23:('Optogenetics makes selected neurons responsive to light',[
'**Optogenetics** combines a light-sensitive protein with a method for placing that protein in selected cells. An **ion channel** is a protein pathway through the cell membrane. When the channel opens, charged particles called ions can cross the membrane.',
'Channelrhodopsin-2, abbreviated **ChR2**, originally comes from an alga. It contains **retinal**, a light-absorbing molecule. Blue light changes the protein so its channel opens. Positive ions moving through the channel can shift the electrical state of a neuron toward firing.',
'The central idea is to connect a controlled change in neural activity with a change in behavior. Choosing the cells and the timing of illumination gives researchers a way to test a circuit’s contribution. Karl Deisseroth, Peter Hegemann, and Georg Nagel received the 2026 Nobel Prize in Physiology or Medicine for optogenetics.']),
24:('Ion movement changes a cell’s electrical state',[
'An **ion** is an atom or molecule carrying electrical charge. Sodium, potassium, and calcium ions carry positive charge; chloride carries negative charge. The cell membrane separates solutions with different concentrations of these ions.',
'An open channel lets some ions move across the membrane. Their movement depends on both the concentration difference and electrical attraction or repulsion. Moving charge changes the **membrane potential**, the voltage difference between the inside and outside of the cell.',
'A channel’s **selectivity** determines which ions pass through it. The source figure compares currents when the surrounding ions change. Optogenetics uses this relationship: light opens the channel, ions move, and the neuron’s electrical state changes.']),
25:('Channel opening gives a neural signal its time course',[
'**Gating** means opening or closing an ion channel. A light-gated channel opens when illumination changes its light-sensitive protein. A voltage-gated channel responds to the membrane voltage instead. Both alter the flow of ions across the membrane.',
'Opening and closing take time. A brief flash can produce a current that persists until the light-sensitive channel closes. The trace in the source figure shows how a rapidly delivered light signal becomes an electrical response with its own time course.',
'Neurons combine signals arriving at different moments. A current can bring the neuron closer to firing, while another current can make firing less likely. The duration of channel opening therefore affects how an experimentally delivered input interacts with the neuron’s other inputs.']),
26:('Depolarization can trigger an action potential',[
'A neuron at rest is usually more negative inside than outside. **Depolarization** makes this voltage difference less negative. An inward flow of positive charge can depolarize the membrane, bringing it toward the voltage at which firing begins.',
'An **action potential** is a brief, self-renewing electrical signal that travels along an axon. Voltage-gated channels open in sequence as the membrane changes voltage. The **axon** carries the signal toward the neuron’s output contacts.',
'At a **synapse**, the output of one neuron influences another cell. Many synapses use chemical messengers called **neurotransmitters**. Optically depolarizing a selected neuron can therefore influence its own firing and the cells receiving its synaptic signals.']),
28:('Excitation and inhibition shape circuit activity',[
'**Excitation** increases a neuron’s tendency to produce action potentials. **Inhibition** reduces that tendency. Neurons receive many inputs, and their combined effects determine whether the cell fires at a particular moment.',
'The effect of an ion channel depends on the ions it carries and the conditions inside and outside the cell. ChR2 carries positive ions. **Anion channelrhodopsins** are light-sensitive proteins that can carry negative ions such as chloride.',
'Optical activation and optical inhibition provide different experimental tools. One can increase firing in selected cells; the other can suppress it under suitable ionic conditions. Comparing the resulting behavior connects the balance of circuit activity with the action being studied.']),
29:('Inhibitory signals change the probability of firing',[
'An inhibitory input can move the membrane voltage away from firing threshold. It can also open an ion pathway that reduces the effect of an excitatory input. Both mechanisms make the neuron less likely to produce an action potential.',
'The direction of chloride movement depends on its concentration and the membrane voltage. Opening a chloride channel drives the membrane toward the voltage at which these forces balance. This voltage is called the **chloride equilibrium potential**.',
'The source trace shows electrical spikes disappearing during illumination of an inhibitory channel. Turning the light off permits firing to resume. This reversible change illustrates how inhibition can regulate when neural signals reach other cells in a circuit.']),
39:('Electrodes turn neural activity into a recorded signal',[
'An **electrode** is a conducting contact used to measure electrical changes. A recording electrode near a neuron detects small voltage changes outside the cell. These **extracellular signals** can reveal when nearby neurons produce action potentials.',
'A recording system measures the signal repeatedly. Its **sampling rate** is the number of measurements each second. Closely spaced measurements capture the brief changes associated with spikes; preserving their order retains information about when neurons were active.',
'The device illustrated here sends recorded signals wirelessly. Researchers can compare these signals with the animal’s position and movement. Combining a neural recording with a behavioral recording connects events in the nervous system with the action occurring at that time.']),
44:('Behavioral measurements start with recognizable body parts',[
'A behavioral description becomes measurable when it identifies an observable feature. A mouse’s snout position describes where its head is pointing; the wrist and digits describe a reaching movement. These **anatomical landmarks** connect a visible structure with the behavior of interest.',
'In a video, a researcher can mark the location of each landmark in selected frames. A computer system can then learn to locate the same features in additional frames. Repeating this across time produces a record of changing body positions.',
'The resulting measurements help distinguish different aspects of an action. Head movement, whole-body movement, and individual digit movement describe different scales of behavior. Selecting a landmark determines which component of the action the measurement explains.']),
63:('Neurons communicate through branching processes',[
'A neuron has a cell body and branching extensions called **processes**. **Dendrites** receive many of its incoming signals. An **axon** carries outgoing electrical signals toward other cells. These structures let one cell participate in a network with many partners.',
'At a chemical synapse, activity in the sending cell causes neurotransmitter release. The transmitter binds to proteins called **receptors** on the receiving cell. The resulting response can change the receiver’s electrical activity and its tendency to fire.',
'The source micrograph shows processes extending across an electrode array. The array contains small conducting contacts that measure nearby voltage changes. These contacts allow an electronic system to communicate with a living network whose own connections distribute signals among cells.']),
65:('Feedback connects an action with its consequence',[
'**Feedback** occurs when the result of an action influences what happens next. During navigation, movement changes the visual scene, and the new scene helps guide the next movement. An animal continuously interacts with the environment through this cycle.',
'A **closed loop** connects measured output to subsequent input. In the cultured-neuron example, neural activity moves a paddle. The resulting ball position changes the electrical stimulation delivered back to the neurons. Output and input are linked through the task.',
'**Learning** involves a relatively lasting change associated with experience. A task that makes consequences depend on the organism’s activity can provide information for adaptation. The source interface makes that relationship explicit by connecting a recorded signal, an action, and the next input.'])}
for n,(title,body) in rows.items():
 x=s['slides'][n-2];x['title']=title;x['body']=body;x['transcript']=body[:];x['instructional_role']='foundation';x['refs']=[BOOK]+x['refs'];x['cite']='Carlson & Birkett (2022); '+x['cite'];x['foundation_basis']='Textbook concept explicitly taught; existing study figure retained as an illustration.'
# Keep evidence and imagery, but make selected research explanations accessible to first-course students.
changes={
27:('Brief light pulses can make neurons fire',[
'Boyden and colleagues placed ChR2 in cultured rat neurons. The light-sensitive protein reached the membrane, where blue light opened a pathway for positive ions. The resulting depolarization could trigger an action potential.',
'A short light pulse could evoke a spike shortly after illumination began. Repeating the pulses gave researchers a way to deliver a timed series of neural inputs. The traces compare the timing of the light pulses with the electrical responses of the cells.',
'Montgomery and colleagues extended light delivery to freely moving mice using a wireless device. Stimulating a premotor region, which helps organize movement, increased circling from about 0.4 to 2.5 turns per minute. Cell-level control becomes a behavioral experiment when the selected activity changes an observable action.']),
30:('Selected fly neurons link light with specific actions',[
'Inagaki and colleagues used **ReaChR**, a light-sensitive channel that responds to longer-wavelength light than ChR2. They expressed it in selected groups of fly neurons. Red illumination could then activate those cells while the animal remained intact.',
'Different groups of neurons were associated with different actions. Activating Gr5a sensory neurons, involved in detecting sugar, elicited extension of the **proboscis**, the fly’s feeding structure. Other targeted groups recruited aspects of courtship and movement.',
'The recording shows the feeding structure extending during illumination. It connects three levels of explanation: a defined neuronal group, a controlled change in its activity, and a recognizable behavioral response. Cell identity determines which action the optical input can recruit.']),
31:('Experience changes how a fly circuit influences courtship',[
'Inagaki and colleagues activated **P1 neurons**, a male fly neuronal group involved in courtship. Courtship includes directed approach and wing movements. These neurons form part of a circuit that connects social information with actions toward another fly.',
'The response depended on the fly’s social history. The same optical manipulation produced different patterns after different housing experiences. Experience therefore changed the relationship between activating a selected group and the courtship behavior that followed.',
'The published recording compares activation of P1 and another courtship-related group called pIP10. The visible wing and body movements make the behavioral output recognizable. Neural activity contributes to action within a circuit whose state also reflects the animal’s previous experience.']),
37:('Fly circuits recruit recognizable movement patterns',[
'**Descending neurons** carry signals from the fly brain toward circuits controlling movement. Cande and colleagues activated selected descending-neuron types and measured changes in behavior. Targeting a cell type connected an identifiable circuit component with a movement pattern.',
'Some activations favored particular behaviors rather than increasing every action equally. The source plots group the behavioral changes produced by different neuronal types. A movement can be described through the organization of the limbs and body over time.',
'The accompanying footage from Grover and colleagues provides visual context for coordinated walking and courtship movements in another fly preparation. The methods differ, but both connect neural circuits with visible behavior. Recognizing the action helps make the recorded neural effect interpretable.']),
40:('Wireless recordings follow brain activity during bat flight',[
'Forli and colleagues recorded neurons while bats flew freely. They studied the **hippocampus**, a brain region involved in memory and spatial representation. A wireless recording system allowed neural measurements to accompany movement through a three-dimensional environment.',
'A **place-related response** occurs when a neuron’s activity varies with the animal’s location. The researchers compared recorded firing with flight position. Activity across a group of neurons described different parts of the route.',
'The important connection is between a changing position and a changing neural signal. Recording during free movement makes it possible to investigate how the brain represents space while an animal uses that space. Later rest recordings examined how patterns related to flight reappeared.']),
41:('Activity during rest can repeat patterns associated with flight',[
'Forli and colleagues compared neural activity during flight with activity during rest. **Replay** refers to a later pattern resembling the order of activity associated with an earlier experience. Here, the comparison used hippocampal signals associated with movement through space.',
'Some rest events repeated sequences related to flight, but over a shorter time. A sequence that occurred during movement could therefore appear in compressed form when the bat was resting. The source figure relates the order of the neural signals across these conditions.',
'The finding connects active navigation with later internal neural activity. The hippocampus can organize patterns when the animal is moving and when it is resting. Comparing those periods helps explain how spatial experience becomes part of an ongoing memory system.']),
42:('Neural representations change across the flight rhythm',[
'Forli and colleagues compared hippocampal activity with repeated movements during flight. A **motor rhythm** is a recurring cycle of movement. In a flying bat, successive wingbeats provide a rhythm against which other measurements can be aligned.',
'The source figure compares spatial representation across phases of this cycle. The recorded signals changed as the movement rhythm progressed. Activity associated with location was therefore organized in time as well as in space.',
'A navigation system must use sensory information while the animal’s body is moving. Relating neural signals to the movement cycle helps connect those processes. The analysis shows how recording both brain activity and behavior can reveal their coordinated timing.']),
62:('Living cultures contain neurons and supporting cells',[
'Kagan and colleagues grew neurons from embryonic mouse cortex and human **induced pluripotent stem cells**, adult cells reprogrammed so they can produce specialized cell types. In culture, neurons extended processes and formed electrically active networks outside the body.',
'The source micrographs identify neuronal cell bodies and their extensions. Cultures also contain **astrocytes**, star-shaped support cells. Astrocytes help maintain the chemical environment around neurons, support metabolism, and participate in signaling associated with synaptic function.',
'The added astrocyte image and recording show this cell type in a separate research preparation. They provide cell-recognition context for the culture discussion. In DishBrain, the connected neural culture supplies the living component whose activity is coupled to a virtual Pong task.']),
70:('A virtual world changes when the animal moves',[
'Stowers and colleagues built virtual environments for freely moving animals. A camera measured the animal’s position, and a computer used that measurement to update the displayed scene. The visual input therefore changed in relation to the animal’s movement.',
'For a fly, moving patterns can recruit an **optomotor response**, a turning response that helps stabilize movement relative to the visual scene. The researchers used this relationship to influence free-flight direction. The recording shows an action-dependent visual environment affecting a recognizable response.',
'The same principle applies across preparations: measure an action, update the sensory input, and measure the next action. This is a closed loop between behavior and the environment. Virtual worlds make the sensory consequences of movement experimentally adjustable.']),
71:('Head position determines the animal’s visual perspective',[
'A nearby object appears in a different direction when an observer moves. Stowers and colleagues tracked the animal’s position so the virtual object could be drawn from the appropriate viewpoint. The displayed scene was updated as that viewpoint changed.',
'**Perspective** describes how a scene appears from an observer’s location. The demonstration recording shows how multiple displays change an object’s appearance as the observer moves. The computer must coordinate those displays with the tracked position.',
'Correctly updating the viewpoint allows movement to supply information about spatial layout. A virtual object can remain in a consistent location in the simulated world even though its image changes on the screens. Sensory guidance depends on this relationship between action and changing visual information.']),
72:('Real and virtual fish can influence each other’s movement',[
'Stowers and colleagues displayed computer-generated partners to real fish. A **virtual partner** is a simulated animal whose appearance and movement can be controlled. The display made the partner visible within the fish’s visual environment.',
'In the social-feedback experiment, the real fish’s position influenced the virtual fish, and the virtual fish’s movement could influence the real fish. The recording shows this reciprocal interaction. Both sides of the loop contribute to the changing visual scene.',
'This arrangement connects social behavior with a controlled sensory relationship. Researchers can vary how strongly the simulated partner follows the real animal. The resulting changes in movement reveal how visual information from another apparent animal contributes to the interaction.'])}
for n,(title,body) in changes.items():
 x=s['slides'][n-2];x['title']=title;x['body']=body;x['transcript']=body[:]
assert sum(x['instructional_role']=='foundation' for x in s['slides'])==29
assert sum(x['instructional_role']=='research' for x in s['slides'])==44
# The title and takeaways remain those of the approved lecture.
(HERE/'lecture.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n')
print('75 slides; 29 substantive foundations and 44 research slides.')
