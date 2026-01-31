# Systematic Literature Review su European Health Data Space (EHDS)
## Versione aggiornata - Gennaio 2026

> **Nota importante**: Il Regolamento (UE) 2025/327 che istituisce l'EHDS è stato adottato l'11 febbraio 2025 ed è entrato in vigore il 26 marzo 2025. Questa versione aggiornata tiene conto del nuovo quadro normativo definitivo.

---

## 1. Articoli recenti e rilevanti su EHDS

### 1.1 Lavori accademici peer-reviewed (2024-2026)

| Titolo | Anno | Fonte | Focus principale |
|--------|------|-------|------------------|
| Anticipating ethical and social dimensions of the European Health Data Space: A rapid systematic review | 2025 | Health Policy (Elsevier) | Rapid review su implicazioni etico-sociali; 7 temi chiave identificati; raccomandazioni policy per governance responsabile |
| Secondary use under the European Health Data Space: setting the scene and towards a research agenda on privacy-enhancing technologies | 2025 | Frontiers in Digital Health | Studio qualitativo (16 interviste esperti) su rischi, sfide e ruolo dei PET; research agenda per integrazione tecnologia-governance |
| The European Health Data Space: An opportunity to strengthen citizen rights and engage citizens in health data governance | 2026 | Frontiers in Medicine | Interviste esperti 23 paesi su opt-out e coinvolgimento cittadini; strategie per engagement nel riuso dati |
| Ethical and social reflections on the proposed European Health Data Space | 2024 | European Journal of Human Genetics (Nature) | Critica etico-normativa al framework per uso secondario; rischi per fiducia pubblica e social licence |
| Will the GDPR Restrain Health Data Access Bodies Under the EHDS? | 2024 | Computer Law & Security Review (Elsevier) | Analisi tensioni GDPR-EHDS; sfide per HDAB nel garantire basi legali per data permits |
| The European Health Data Space: An expanded right to data portability? | 2023 | Computer Law & Security Review (Elsevier) | Confronto Art. 3(8) EHDS vs Art. 20 GDPR; limiti della portabilità per uso secondario |
| Interoperability Framework of the EHDS for Secondary Use: Interactive EIF-Based Standards Compliance Toolkit for AI-Driven Projects | 2025 | Journal of Medical Internet Research | Framework interoperabilità basato su EIF; toolkit per compliance progetti AI con EHDS2 |
| Reality Check: The Aspirations of the EHDS Amidst Challenges in Decentralized Data Analysis | 2025 | Journal of Medical Internet Research | Sfide tecniche e legali per federated/swarm learning nell'EHDS; gap tra ambizioni e realtà |
| User journeys in cross-European secondary use of health data: insights ahead of the EHDS | 2025 | European Journal of Public Health (Oxford) | Case study su accesso dati in 4 paesi; barriere pratiche pre-EHDS |
| The European Health Data Space as a Case Study | 2024 | Ethics & Human Research (Wiley) | Approccio translational bioethics; critica ai meccanismi opt-out e governance |
| Preparing for the EHDS: An Open-Source Compiler for Fast, Transparent, and Portable Health Data Transformations | 2025 | Frontiers in Medicine | Strumento MaLaC-HD per trasformazione dati; supporto interoperabilità FHIR |
| Common European Data Spaces in Health Care: A Privacy-Preserving Ecosystem for Cancer Research | 2026 | Springer LNBIP (DSPE 2025) | Framework privacy-preserving per ricerca oncologica; integrazione PET e governance |
| Shaping the future EHDS: recommendations for HDAB implementation in HealthData@EU infrastructure | 2025 | European Journal of Public Health (Oxford) | Raccomandazioni pratiche per HDAB basate su HealthData@EU Pilot |
| European Health Data Space—An Opportunity Now to Grasp the Future of Data-Driven Healthcare | 2022 | Healthcare (MDPI) | Analisi multistakeholder; equilibrio governance vs innovazione |
| Evaluating Legal Compliance of Federated Learning Tools for the EHDS | 2024 | IEEE FLTA 2024 Conference | Valutazione compliance GDPR di strumenti FL per EHDS |
| FED-EHR: A Privacy-Preserving Federated Learning Framework for Decentralized Healthcare Analytics | 2025 | Electronics (MDPI) | Framework FL per analisi decentralizzate in conformità GDPR/EHDS |
| From Challenges and Pitfalls to Recommendations: Implementing Federated Learning in Healthcare | 2024/2025 | arXiv / NPJ Digital Medicine | Review sistematica FL in sanità; sfide implementative e bias |
| Privacy-Preserving Heterogeneous Federated Learning for Sensitive Healthcare Data | 2024 | arXiv | Framework AAFV per FL eterogeneo con differential privacy |

### 1.2 Report, policy brief, grey literature (2024-2026)

| Titolo | Anno | Fonte | Contenuto chiave |
|--------|------|-------|------------------|
| TEHDAS2 Joint Action | 2024-2026 | Sitra/EU4Health | Supporto implementazione EHDS; linee guida per HDAB, opt-out, data quality |
| Draft Guideline: How to implement opt-out from secondary use | 2025 | TEHDAS2 | Raccomandazioni operative per meccanismi opt-out nazionali |
| EFPIA Position on opt-out in the EHDS Regulation | 2024 | EFPIA | Sfide operazionalizzazione opt-out; rischi frammentazione |
| European Health Data Space (EHDS): A Comprehensive Guide | 2025 | IQVIA White Paper | Impatti strategici per industria; requisiti implementazione |
| Policy Brief: The EHDS – from approval to national implementation | 2024 | GA4GH | Margini nazionali, IP, dati genetici |
| HealthData@EU Pilot Final Outputs | 2024 | EU Commission | Lezioni apprese; raccomandazioni infrastruttura |
| European Health Data Space – Data Quality Framework | 2022 | TEHDAS | Framework qualità dati per riuso secondario |
| EHDS White Paper Portugal | 2024 | EIT Health | Action toolkit per stakeholder nazionali |
| Getting ready for the EHDS: IDERHA's plan | 2024 | Open Research Europe | Allineamento progetti ricerca con requisiti EHDS2 |

---

## 2. Filoni tematici e ipotesi per la SLR

### 2.1 Asse 1 — Governance, diritti, etica

#### Domande di ricerca (RQ)

- **RQ1**: Come il Regolamento EHDS (2025/327) ridefinisce il bilanciamento tra promozione dell'uso secondario e tutela dei diritti fondamentali (privacy, autonomia, non-discriminazione) rispetto al quadro GDPR?
- **RQ2**: In che misura i meccanismi di opt-out (Art. 71) e il ruolo degli HDAB sono percepiti come sufficienti a garantire fiducia pubblica e legittimità democratica?
- **RQ3**: Quali questioni etico-sociali emergono nella letteratura post-adozione e come vengono tradotte in raccomandazioni di policy?

#### Ipotesi di lavoro

- **H1**: La letteratura continua a enfatizzare i rischi di erosione dell'autonomia individuale nonostante l'introduzione dell'opt-out, evidenziando un persistente gap di legittimazione sociale dell'EHDS.
  - *Evidenze*: Staunton et al. (2024) sottolineano i rischi per la social licence; van Drumpt et al. (2025) evidenziano che la fiducia pubblica dipende dalla trasparenza più che dal rispetto formale del GDPR.

- **H2**: I modelli di governance degli HDAB presentano rischi di colli di bottiglia e asimmetrie di capacità tra Stati membri, con potenziale "data colonialism" intra-UE.
  - *Evidenze*: Forster et al. (2025) documentano tempi di accesso dati molto diversi tra paesi; la letteratura anticipa che paesi con bassa digitalizzazione saranno svantaggiati (Health Policy 2025).

- **H3**: L'opt-out, pur rispondendo a preoccupazioni democratiche, introduce complessità operative che potrebbero frammentare l'effettivo funzionamento del data space paneuropeo.
  - *Evidenze*: EFPIA Position (2024) solleva preoccupazioni su frammentazione; TEHDAS2 Guideline (2025) riconosce sfide implementative significative.

---

### 2.2 Asse 2 — Uso secondario, PET e infrastruttura tecnica

#### Domande di ricerca (RQ)

- **RQ4**: Quali modelli di uso secondario dei dati sanitari vengono abilitati dall'EHDS e quali barriere tecnico-regolatorie persistono dopo l'adozione del Regolamento?
- **RQ5**: Come la letteratura valuta la capacità delle PET (federated learning, secure processing environments, differential privacy) di mitigare i rischi mantenendo l'utilità dei dati?
- **RQ6**: Quali framework di qualità del dato e interoperabilità vengono proposti per rendere effettivo il riuso transfrontaliero?

#### Ipotesi di lavoro

- **H4**: Esiste un significativo disallineamento tra le ambizioni di riuso su larga scala e la maturità operativa delle PET, specialmente per analisi multi-paese.
  - *Evidenze*: Fröhlich et al. (2025 JMIR) evidenziano che federated/swarm learning richiedono infrastrutture robuste ancora non disponibili; van Drumpt et al. (2025) confermano che le PET da sole non possono sostituire una governance forte.

- **H5**: Le raccomandazioni su data quality e interoperabilità (TEHDAS, EIF) sono ancora poco integrate nei lavori giuridico-etici, creando una frattura tra discorso tecnico e regolatorio.
  - *Evidenze*: Hussein et al. (2025) propongono toolkit per colmare questo gap; la letteratura etica raramente affronta aspetti tecnici specifici.

- **H6**: I progetti pilota (HealthData@EU, EHDS2) dimostrano che le principali barriere non sono tecniche ma organizzative: governance multi-attore, sostenibilità economica, capacity building.
  - *Evidenze*: Forster et al. (2025) documentano che le variazioni nei tempi di accesso dipendono da processi istituzionali, non da limiti tecnici.

---

### 2.3 Asse 3 — Implementazione nazionale e variabilità tra Stati membri

#### Domande di ricerca (RQ)

- **RQ7**: Come si prevede che gli Stati membri implementino l'EHDS e quali variabili condizionano le traiettorie di attuazione?
- **RQ8**: Quali rischi di aumento delle disuguaglianze tra Stati membri emergono e quali correttivi sono suggeriti?

#### Ipotesi di lavoro

- **H7**: L'EHDS, pur mirato a ridurre la frammentazione, può inizialmente amplificare le differenze tra paesi con diversa capacità di gestione dati, con rischi di "data colonialism" intra-UE.
  - *Evidenze*: Health Policy (2025) identifica impatti sproporzionati su Stati con sfide di digitalizzazione; Estonia vs altri paesi come esempio di divario.

- **H8**: Gli Stati membri ricorreranno ampiamente ai margini nazionali di restrizione (Art. 33(5) per dati genetici e categorie sensibili), limitando l'estensione reale del data space paneuropeo.
  - *Evidenze*: Arnold & Porter (2025) nota che alcuni Stati (es. Francia) hanno già indicato preferenze per restrizioni più stringenti.

- **H9 (NUOVA)**: La timeline di implementazione (marzo 2027-2031) creerà un periodo di incertezza normativa durante il quale le organizzazioni dovranno operare con regole parzialmente definite.
  - *Evidenze*: Il Regolamento richiede numerosi atti delegati e di esecuzione (deadline 2027) prima della piena applicabilità.

---

### 2.4 Asse 4 — Coinvolgimento dei cittadini e public value

#### Domande di ricerca (RQ)

- **RQ9**: Quali modelli di coinvolgimento dei cittadini vengono proposti e implementati nel contesto EHDS?
- **RQ10**: Come viene concettualizzato e misurato il "valore pubblico" generato dall'EHDS?

#### Ipotesi di lavoro

- **H10**: L'architettura dell'EHDS rimane principalmente top-down, con un coinvolgimento dei cittadini più simbolico che sostanziale nella governance del riuso dati.
  - *Evidenze*: Dove (2024) nota che la consultazione pubblica pre-EHDS ha raccolto solo ~100 risposte da cittadini; Frontiers (2026) suggerisce necessità di strategie engagement più robuste.

- **H11**: I lavori orientati al valore pubblico enfatizzano maggiormente benefici macro (ricerca, innovazione, €11 miliardi di risparmi stimati) che benefici percepibili dal singolo paziente.
  - *Evidenze*: EY (2025) quantifica benefici economici aggregati; manca letteratura su perceived value a livello individuale.

---

### 2.5 Asse 5 — Federated Learning e tecnologie emergenti (NUOVO)

#### Domande di ricerca (RQ)

- **RQ11**: Come il Federated Learning si posiziona come soluzione tecnica per l'EHDS e quali sono le sue limitazioni specifiche nel contesto sanitario europeo?
- **RQ12**: Quali gap esistono tra la ricerca accademica sul FL e l'implementazione operativa nell'EHDS?

#### Ipotesi di lavoro

- **H12**: Il FL è promettente ma la sua compliance legale con GDPR/EHDS non è ancora completamente chiarita, specialmente per quanto riguarda lo status dei gradienti e dei modelli aggregati.
  - *Evidenze*: IEEE FLTA 2024 conference paper; Jacquemin (2025 VUB) discute incertezze su status anonimo dei risultati aggregati.

- **H13**: La maggior parte degli studi sul FL in sanità presenta limiti metodologici significativi che ne compromettono l'utilità clinica reale.
  - *Evidenze*: arXiv review (2024/2025) identifica bias, problemi di generalizzazione, costi di comunicazione come barriere pervasive.

---

## 3. Timeline normativa EHDS (aggiornata)

| Data | Milestone |
|------|-----------|
| 3 maggio 2022 | Proposta Commissione Europea |
| 15 marzo 2024 | Accordo politico Parlamento-Consiglio |
| 24 aprile 2024 | Adozione Parlamento Europeo |
| 21 gennaio 2025 | Adozione definitiva Consiglio |
| 5 marzo 2025 | Pubblicazione GUUE |
| 26 marzo 2025 | **Entrata in vigore** Reg. (UE) 2025/327 |
| Giugno 2025 | Nomina Digital Health Authorities nazionali |
| Marzo 2027 | Deadline atti delegati/di esecuzione Commissione |
| Marzo 2029 | Applicazione uso primario (Patient Summary, ePrescription) e uso secondario (maggior parte categorie) |
| Marzo 2031 | Applicazione dati genetici, trial clinici, imaging, risultati laboratorio |

---

## 4. Suggerimenti metodologici per la SLR

### 4.1 Strategia di ricerca per database

| Database | Focus tematico | Keyword suggerite |
|----------|---------------|-------------------|
| IEEE Xplore | PET, architetture tecniche, FL, secure computing | "EHDS" AND ("federated learning" OR "privacy-enhancing" OR "secure multiparty") |
| Frontiers | Prospettive stakeholder, citizen engagement, digital health | "European Health Data Space" AND (citizen OR governance OR implementation) |
| MDPI | Health informatics, data governance, interoperabilità | "EHDS" AND (interoperability OR "data quality" OR governance) |
| Elsevier/ScienceDirect | Giuridico-etico, policy, GDPR | "European Health Data Space" AND (GDPR OR ethics OR "secondary use") |
| Springer/Nature | Bioetica, genetica, riflessioni normative | "EHDS" AND (ethical OR genetic OR bioethics) |
| Oxford Academic | Public health, epidemiologia, user journeys | "European Health Data Space" AND (public health OR cross-border) |
| arXiv | Preprint tecnici, FL, privacy | "health data" AND ("federated learning" OR "differential privacy") AND Europe |
| PubMed/PMC | Applicazioni cliniche, medical informatics | "European Health Data Space"[All Fields] |

### 4.2 Framework di codifica

Categorie principali per analisi tematica:

1. **Diritti e autonomia**: consenso, opt-out, portabilità, controllo individuale
2. **Governance e istituzioni**: HDAB, EHDS Board, Stakeholder Forum, rapporti Stato-UE
3. **Infrastruttura tecnica**: MyHealth@EU, HealthData@EU, PET, interoperabilità, EHR
4. **Qualità dei dati**: FAIR principles, standardizzazione, completezza, accuratezza
5. **Equità e inclusione**: digital divide, capacità nazionali, popolazioni vulnerabili
6. **Coinvolgimento pubblico**: engagement cittadini, trasparenza, valore percepito
7. **Impatti settoriali**: ricerca, industria, policy-making, assistenza clinica

### 4.3 Criteri di inclusione/esclusione suggeriti

**Inclusione**:
- Pubblicazioni 2022-2026 (dal lancio proposta EHDS)
- Focus esplicito su EHDS o diretto predecessore (MyHealth@EU, TEHDAS)
- Peer-reviewed journals, conference proceedings, working papers istituzionali
- Grey literature da istituzioni UE, joint actions, associazioni di categoria

**Esclusione**:
- Articoli pre-2022 su data sharing sanitario senza riferimento a EHDS
- News articles, blog posts senza rigore metodologico
- Documenti puramente tecnici senza implicazioni policy/etiche (salvo asse tecnico)

---

## 5. Collegamento con il paper FLaaS per il contesto italiano

Il paper "Federated Learning as a Service for Italian Healthcare" (allegato al progetto) si colloca all'incrocio di diversi assi della SLR:

- **Asse 2 (PET)**: Propone FLaaS come soluzione tecnica specifica per contesti frammentati
- **Asse 3 (Implementazione nazionale)**: Analizza peculiarità italiane (regionalizzazione, FSE 2.0, PNRR)
- **Asse 5 (FL)**: Fornisce framework implementativo concreto per FL in sanità

Le ipotesi del paper possono essere validate/confutate attraverso la SLR:
- La frammentazione regionale italiana come caso estremo di sfida implementativa EHDS
- Il modello FLaaS come possibile pattern replicabile in altri Stati membri frammentati
- Il ruolo del FSE 2.0 come infrastruttura abilitante per compliance EHDS

---

## Riferimenti bibliografici principali

1. Staunton, C., Shabani, M., Mascalzoni, D., et al. (2024). Ethical and social reflections on the proposed European Health Data Space. *European Journal of Human Genetics*, 32(5), 498-505.

2. van Drumpt, S., Chawla, K., Barbereau, T., et al. (2025). Secondary use under the European Health Data Space: setting the scene and towards a research agenda on privacy-enhancing technologies. *Frontiers in Digital Health*, 7, 1602101.

3. Quinn, P., Ellyne, E., & Yao, C. (2024). Will the GDPR restrain health data access bodies under the EHDS? *Computer Law & Security Review*, 54, 105993.

4. Hussein, R., Gyrard, A., Abedian, S., et al. (2025). Interoperability Framework of the EHDS for Secondary Use. *Journal of Medical Internet Research*, 27, e69813.

5. Fröhlich, H., Hansen, A.F., Hilvo, M., et al. (2025). Reality Check: The Aspirations of the EHDS Amidst Challenges in Decentralized Data Analysis. *Journal of Medical Internet Research*, 27, e76491.

6. Forster, R.B., Garcia Alvarez, E., Zucco, A.G., et al. (2025). User journeys in cross-European secondary use of health data. *European Journal of Public Health*, 35(Suppl 3), iii18-iii24.

7. Dove, E.S. (2024). The European Health Data Space as a Case Study. *Ethics & Human Research*, 46(6), 2-11.

8. Dalmolen, S., van Hillegersberg, J., et al. (2026). Common European Data Spaces in Health Care: A Privacy-Preserving Ecosystem. *Lecture Notes in Business Information Processing*, 563.

9. TEHDAS2 Joint Action. (2025). Draft Guideline: How to implement opt-out from secondary use of electronic health data.

10. European Commission. (2025). Regulation (EU) 2025/327 on the European Health Data Space. *Official Journal of the European Union*, L 2025/327.
