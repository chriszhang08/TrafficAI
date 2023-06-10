# TrafficAI

- [Project summary](#project-summary)
  - [The issue we are hoping to solve](#the-issue-we-are-hoping-to-solve)
  - [How our technology solution can help](#how-our-technology-solution-can-help)
  - [Our idea](#our-idea)
- [Technology implementation](#technology-implementation)
  - [IBM Watson Studio](#machine-learning-component)
  - [IBM AI service(s) used](#ibm-ai-services-used)
  - [Solution architecture](#solution-architecture)
- [Presentation materials](#presentation-materials)
  - [Solution demo video](#solution-demo-video)
  - [Project development roadmap](#project-development-roadmap)
  - [Future prospects](#future-prospects)
  - [Business Model](#business-model)
  - [Tutorial and Interface](#tutorial-documentation)
- [About this template](#about-this-template)
  - [Authors](#authors)

## Project summary

The world is undergoing one of the largest waves of urban growth in history. With that growth has come an exponential increase in population and vehicles on the roads. Existing roads, however, either do not have the capacity for high numbers of cars or are poorly designed due to lacking design technology, leading to traffic congestion. This build-up of stopped vehicles is detrimental to the environment as vehicles continue to emit carbon dioxide while they wait in traffic for hours. Although a lot of advances have been made to make cars pollute less, little attention has been paid to efforts to make cars drive less. Through machine learning, our team strives to simulate traffic conditions and obtain insights to determine optimal road configurations: road network structure, road signage location, and highway exit orientation. With these insights, our team strives to help reduce traffic carbon emissions and build smarter, eco-friendly cities.


This is how our solution, Traffic AI, can make an impact.

### The issue we are hoping to solve

We aim to reduce the carbon dioxide vehicles emit into the environment by decreasing traffic congestion. Moreover, we aim to develop technology that contributes to smart cities through self-driving car traffic coordination, further reducing carbon dioxide emissions. With our program, civil engineers and urban planners will have a data-driven tool to minimize traffic congestion.

### How our technology solution can help

Our solution will leverage machine learning to simulate traffic flow and analyze various parameters, including vehicle flow, congestion patterns, and carbon emission levels, to provide valuable insights that help predict efficient road networks and road signage.

### Our idea

Traffic is dreaded by many on their work commutes, school drop-offs, and daily errands. On average, each person spends 54 hours in traffic; some cities, such as Chicago, averaging at 155 hours per person. However, besides being inconvenient, traffic is a significant source of greenhouse gas emissions. As people wait in traffic, their vehicles continue to emit greenhouse gasses, annually releasing 63,000 metric tons of CO2 in the US alone. Our team aims to determine the most efficient road configuration and signaling using artificial intelligence. By providing contractors, consultants, and governments with this technology, new road systems can be optimized and existing roads can be analyzed to determine congestion-relieving strategies, reducing traffic holistically.  

A variety of factors cause traffic, one of them being saturation, which means that roads can not handle the number of vehicles that drive through them. Exit locations, number of lanes, and stoplight designs all play a role in potential road saturation. Another cause of traffic is poor road signaling. Abruptly closed lanes, hidden highway exits, and unannounced construction zones are all reasons why unnecessary traffic may be formed. Our technology targets all these traffic factors in order to mitigate them through efficient road system designs and strategic road signaling. 

Unlike current traffic simulators, our technology leverages the powers of artifical intelligence to simulate thousands of scenarios for any highway intersection. As the program is trained through these scenarios, it uses vehicle flow, congestion patterns, and preexisting highway configurations as parameters to deliver accurate insights on the efficiency of that highway configuration. For new road designs, users can input a location list and an estimated number of cars into the program, allowing the program to determine the optimal road network between the given locations. The program would take existing buildings, roads, and parks into account in order to generate a realistic road system that complements current infrastructure. Moreover, given that the US alone has more than 4 million miles of currently existing roads, our team wanted to address traffic in these existing areas as well, further making our technology unique. With our technology, users can improve current systems through better road signaling of highway exits, closed lanes, construction zones, etc. The program uses Pygame to simulate current road systems, so users are able to specify inputs such as obstacles and estimated vehicle count. Then, the model can simulate different signaling locations to notify the user which is most efficient and capable of minimizing carbon emissions.

## Technology implementation

### Machine Learning component

IBM Watson Studio Project can be found [here](https://dataplatform.cloud.ibm.com/analytics/notebooks/v2/df48d8cc-59d2-4e2b-b5ef-9035b2400c0a/view?projectid=aac45297-1e43-4e0d-a403-24c809aae8e1&context=cpdaas)

### IBM AI service(s) used

- [IBM Watson Studio](https://cloud.ibm.com/catalog/services/watson-studio?catalog_query=aHR0cHM6Ly9jbG91ZC5pYm0uY29tL2NhdGFsb2c%2FY2F0ZWdvcnk9YWkjc2VydmljZXM%3D) - Deploying the machine learning notebook that leverages IBMs computing capabilities.

- [IBM API Connect](https://www.ibm.com/products/api-connect?utm_content=SRCWW&p1=Search&p4=43700074478134124&p5=p&gclid=Cj0KCQjw_r6hBhDdARIsAMIDhV_qr7-DmFAWMWnLiHyMNizro5w2HrcTW40IB6TOQoJXVDooFY0VXVsaAlN2EALw_wcB&gclsrc=aw.ds) - Securly managing the various APIs that will be used to help train and test the model.

## Presentation materials

### Solution demo video

// TODO

### Solution architecture

![TrafficAI-Page-1 drawio](https://github.com/chriszhang08/TrafficAI/assets/52334278/88c484a6-a4f8-456a-8cc9-aee37cd8c4ee)
1. Federal Highway Administration Traffic API will help the model simulate traffic in real-time, allowing for greater accuracy.
2. Utilizing existing traffic models and research will improve the accuracy of AI model by allowing it to iterate through a larger set of traffic configurations.
3. A curated database of previous traffic scores and other internal data points relevant to the AI.
4. The user of the application in this solution architecture is any stakeholder who has a say over the development of the civil infrastructure.
5. The simulation controls the environment that the AI model acts in.
6. Proprietary data about current highway configurations, nationwide vehicle statistics, TrafficAI performance metrics, and any other relevant historic data.
7. The application will consult with civil engineers and urban planners to design an interface that is convenient for everyone and easily adoptable.
8. The knowledge catalog will be used to deliver data driven insights on enterprise data.
9. The core of the entire application is the AI model itself - everything feeds into the training and development of the model.

### Project development roadmap
<img width="778" alt="Screenshot 2023-06-09 230157" src="https://github.com/chriszhang08/TrafficAI/assets/130103153/2b0dad0a-eff4-4855-9fca-69ff0ead20cb">



### Future prospects
As we continue to develop this technology, our team will integrate features that make car behavior more accurate, such as patterns in popular locations at certain times and implementing various driver archetypes. Since these features are associated with the user inputs and not the core framework, these additions will be seamless for users. Furthermore, we hope our program can expand into the autonomous car field, where our program could be used to help coordinate self-driving vehicles to reduce traffic. Finally, we hope to integrate this technology to improve navigation software, creating an ecosystem where these softwares can become smartly aware of the other cars that share the same roads.

### Business Model
<img width="476" alt="Traffic AI Business model" src="https://github.com/chriszhang08/TrafficAI/assets/130103153/f0ae30ec-c527-4f7b-95e8-2fd5730cc490">

### Tutorial Documentation
#### What is Traffic AI?

Traffic AI is a software we created which leverages IBM's AI technologies and machine learning algorithms to simulate and analyze factors such as traffic flow, congestion patterns, and carbon emissions. By outputting data-driven insights, civil engineers and urban planners can make informed decisions to minimize traffic congestion and also build efficient traffic road networks.

#### Key Features of Traffic AI:

Intelligent Traffic Simulations - Traffic AI leverages machine learning to generate and evaluate multiple traffic scenarios. Using multiple parameters that can be factored into the program including vehicle flow, carbon emission levels, and congestion levels, the program delivers optimal results for different road configuration.
Optimal Road Network Design - By considering existing infrastructure, Traffic AI can design road systems that both reduce carbon emissions and also integrate with the current environment. It is very valuable for new road designs or expanding existing networks.
Real-time Road Signaling - Traffic AI improves existing roads by suggesting optimal road signaling including road signs, highway exit orientation, and construction control signing in real-time.

#### Tutorial: How to Use Traffic AI
<img width="1512" alt="IMG_3890" src="https://github.com/chriszhang08/TrafficAI/assets/130103153/78669fc8-52a7-45f9-b9a7-efc9d6ef55df">


Using Traffic AI is a very straightforward process. The only requirement on the user's part is to specify hyperparameters that describe a certain road system or location. Once the software is launched, it will ask the user to seelct relevant parameters, including but not limited to points of interest, traffic congestion data, vehicle flow, carbon emission levels, and more. This data allows the program to iterate through thousands of scenarios to generate an optimal network design or output the best steps when it comes to traffic signaling.

Once the parameters have been specified, Traffic AI uses machine learning algorithms, specifically reinforcement learning, to simulate multiple traffic scenarios and analyze the parameters/requests provided by the user. It will then simulate different road configurations, constantly varying factors such as the number of lanes in the system, the length of the entry and exit ramps, and so much more in order to determine the most optimal design; this layout corresponds to a system in which the least amount of carbon emissions are produced and the most efficient vehicle travel time is calculated.

The user can also manually interact with the simulator and program to explore different possibilities such as closed lanes, construction zones, and any other factors impacting traffic flow. As previously noted, the unsupervised reinforcement models built to identify the single best traffic configuration will be used to guide the creation and development of road systems. 

By following this tutorial and engaging with Traffic AI, users can take advantage of endless datapoints and insights, ultimately contributing to less congested traffic systems and more sustainable cities.

Finally, it is worth noting that Traffic AI will have 24/7 support available for help with any questions or concerns.


---

### Authors

- **Chris Zhang**
- **Natalia Alejo**

#### References

[1] “Nagel–schreckenberg model,” Wikipedia, [https://en.wikipedia.org/wiki/Nagel%E2%80%93Schreckenberg_model] (accessed May 27, 2023).

[2] P. J. Wright, “Investigating traffic flow in the Nagel-schreckenberg model - Researchgate,” Investigating Traffic Flow in The Nagel-Schreckenberg Model, [https://www.researchgate.net/publication/257392971_Investigating_Traffic_Flow_in_The_Nagel-Schreckenberg_Model (accessed May 27, 2023)].
