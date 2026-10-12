from pathlib import Path
import json,re,copy
HERE=Path(__file__).resolve().parent;s=json.loads((HERE/'lecture.json').read_text())
BOOK='Carlson NR, Birkett MA (2022). Physiology of Behavior, Global Edition, 13th edition. Pearson. ISBN 9781292430256.'
DOGRA='Dogra D, Phan VA, Zhang S, Gavrilovici C, DiMarzo N, Narang A, Ibhazehiebo K, Kurrasch DM, Kim E (2025). Modulation of NMDA receptor signaling and zinc chelation prevent seizure-like events in a zebrafish model of SLC13A5 epilepsy. PLoS Biology 23(4):e3002499. https://doi.org/10.1371/journal.pbio.3002499'
NAV='Navarrete M, Perea G, Fernandez de Sevilla D, Gómez-Gonzalo M, Núñez A, Martín ED, Araque A (2012). Astrocytes mediate in vivo cholinergic-induced synaptic plasticity. PLoS Biology 10(2):e1001259. https://doi.org/10.1371/journal.pbio.1001259'
INA=s['slides'][30-2]['refs'][0]
VR=s['slides'][70-2]['refs'][0]
LANC='Lancaster MA, Renner M, Martin CA, Wenzel D, Bicknell LS, Hurles ME, Homfray T, Penninger JM, Jackson AP, Knoblich JA (2013). Cerebral organoids model human brain development and microcephaly. Nature 501:373–379. https://doi.org/10.1038/nature12517'
# Foundation concepts and experiments are connected in prose without textbook metacommentary.
x=s['slides'][3-2];x['title']='Abnormal neural activity and recovery reveal plasticity';x['body']=[
'A **seizure** is a period of abnormal neural activity that can disrupt awareness, sensation, or movement. Its behavioral effects depend on the brain systems involved. Rasmussen encephalitis is an inflammatory condition that can cause repeated seizures arising from one cerebral hemisphere.',
'A **hemisphere** is one of the two large sides of the cerebrum. In severe childhood cases, disconnecting the affected hemisphere can reduce seizures. **Plasticity**, the capacity of neural systems to reorganize, helps explain how remaining circuits can support recovery with development and rehabilitation.',
'Neural activity can also be examined in experimental seizure models. Dogra and colleagues used a fluorescent calcium indicator in larval zebrafish with altered citrate-transport genes. The recording shows calcium events in the midbrain of an epilepsy-related model, connecting abnormal excitability with a visible cellular signal.'];x['refs']+=[DOGRA];x['cite']+='; Dogra et al. (2025)'
x=s['slides'][6-2];x['body'][2]=x['body'][2].replace('the textbook idea of organized brain function','organized brain function')
x=s['slides'][12-2];x['body'][0]=x['body'][0].replace('in the textbook’s discussion of neuroscience','in a biological account');x['body'][1]=x['body'][1].replace('The textbook presents this proposal as a historical explanation.','Later investigations related mental functions to observable brain structures and physiological processes.')
x=s['slides'][18-2];x['body'][1]=x['body'][1].replace('The textbook’s primate tree','The primate tree')
# Aesthetic animal recordings now accompany the specific visible trait under discussion.
x=s['slides'][10-2];x['body'][2]='A barreleye fish provides another example of structure serving a sensory function. The recording shows its transparent head region and conspicuous eyes. Locating sensory structures within the living animal connects anatomical organization with the visual information available in its environment.'
x=s['slides'][15-2];x['body'][2]='Dragonfish illustrate how unusual visible traits can occur in an animal’s normal environment. The recording shows the body and light-producing structures of a deep-sea fish. Natural selection concerns inherited differences affecting survival and reproduction across generations; the living animal provides context for asking how a trait functions.'
x=s['slides'][16-2];x['body'][2]='The vampire squid footage shows another animal with structures suited to its surroundings. Its arms and fine filaments provide recognizable features to investigate. Functional explanations connect such structures with what the animal does, while mechanistic explanations investigate the sensory and motor processes involved.'
x=s['slides'][37-2];x['body'][2]='A separate preparation from Inagaki and colleagues shows sideways walking when light activates neurons labeled by the HB9 driver. These are different targeted cells from the descending-neuron study. The footage supplies movement-recognition context: circuit activation changes the organization of a visible motor action.';x['refs']+=[INA];x['cite']+='; Inagaki et al. (2014)'
x=s['slides'][20-2];x['body'][2]='Developing nervous systems contain dividing precursor cells as well as differentiating neurons. In Lancaster and colleagues’ cerebral organoids, live imaging follows nuclei moving within a developing tissue. A **cerebral organoid** is a three-dimensional culture reproducing selected features of early brain development.';x['refs']+=[LANC]
x=s['slides'][65-2];x['body'][2]='The virtual-aquarium demonstration provides the same general relationship in a freely swimming fish: movement changes the displayed scene. In the neural-culture task, recorded activity changes the paddle and the next stimulation. These examples connect feedback with sensory input that depends on the system’s own action.';x['refs']+=[VR]
x=s['slides'][44-2];x['body'][2]='The mouse-head recording from Stowers and colleagues shows a detected head location marked in green. The detected body outline and center appear in magenta. Recognizable landmarks turn a visible action into positions that a computer can use to update the animal’s sensory environment.';x['refs']+=[VR];x['cite']+='; Stowers et al. (2017)'
x=s['slides'][62-2];x['refs']+=[NAV,BOOK]
# New intact, labeled source imagery supplements rather than replaces the existing panels.
def bookfig(name,num,pdf,printed,description):return {'path':'figures/'+name,'kind':'textbook','isbn':'9781292430256','pdf_page':pdf,'printed_page':printed,'figure_id':num,'caption':f'Carlson and Birkett (2022), Fig. {num}, p. {printed}. '+description,'source_url':'https://books.google.com/books?vid=ISBN9781292430256'}
neuron=bookfig('neuron_anatomy.png','2.4',41,40,'Labeled cell body, dendrites, axon, and terminals.')
astro=bookfig('astrocyte_anatomy.png','2.10',45,44,'Astrocytes, neurons, and metabolic support.')
central=bookfig('central_peripheral.png','2.1',39,38,'Brain, spinal cord, and peripheral nerves.')
astrophoto={'path':'figures/astrocyte_micrograph.png','kind':'article','caption':'Navarrete et al. (2012), Fig. 1A. Fluorescently labeled astrocytes and calcium-indicator signal; original 20 µm scale bar.','source_url':'https://doi.org/10.1371/journal.pbio.1001259'}
seizurefig={'path':'figures/seizure_calcium.png','kind':'article','caption':'Dogra et al. (2025), Fig. 6A–C. Calcium-event measurements and a single-neuron trace in a zebrafish epilepsy model.','source_url':'https://doi.org/10.1371/journal.pbio.3002499'}
added=[]
for n,fig in [(2,neuron),(4,central),(9,astro),(14,neuron),(26,neuron),(62,astrophoto),(63,neuron),(3,seizurefig)]:
 x=s['slides'][n-2];assert 'figure' in x
 x['figures']=[x.pop('figure'),copy.deepcopy(fig)];x['layout']='figures-right';x['figure_width']=5.7;x['primary_figure_height']=2.3
 if fig['kind']=='textbook' and BOOK not in x['refs']:x['refs'].append(BOOK)
 added.append({'original_slide':n,'figure':fig})
for x in s['slides']:
 x['transcript']=x['body'][:]
 
 for b in x['body']:
  if 'textbook' in b.lower():raise ValueError((x['title'],b))
# Interleave concept, mechanism, and study instead of a long foundations-first block.
order=[2,8,48,49,50,51,52,53,9,10,4,13,14,3,5,6,7,11,12,15,16,32,33,17,18,19,20,68,69,21,54,55,56,57,58,59,60,61,22,23,24,25,26,27,28,29,30,31,37,34,35,36,38,39,40,41,42,44,43,45,46,47,63,62,64,65,66,67,70,71,72,73,74]
assert sorted(order)==list(range(2,75))
map_={old:new for new,old in enumerate(order,2)}
s['slides']=[s['slides'][i-2] for i in order]
s['revision_note']='Version 2: interwoven foundations and research, clear introductory mechanisms, original scientific figures retained, concept-matched media.'
(HERE/'slide_order.json').write_text(json.dumps({'original_to_v2':map_,'original_order':order},indent=2)+'\n')
(HERE/'added_images.json').write_text(json.dumps(added,indent=2,ensure_ascii=False)+'\n')
(HERE/'lecture.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n')
print('Interleaved 29 foundations / 44 research slides; preserved all original source figures and added 8 source images.')
