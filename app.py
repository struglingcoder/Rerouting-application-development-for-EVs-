from flask import Flask, request, render_template 
import networkx as nx
import gmplot

e = [('a','b',1),('b','c',2),('a','c',3),('ce','d',4),('d','e',2),('b','e',1)]

def threshold(S_D_dis, Battery, Mileage, Dis_des_near_cs):
    max_pos_dis = Battery * Mileage / 100
    if ((max_pos_dis - S_D_dis)>Dis_des_near_cs):
        return True
    elif ((max_pos_dis - S_D_dis)<Dis_des_near_cs):
        return False

def shortest_path(sp,fd,cs,charging,data) :

    G = nx.Graph()
    G.add_weighted_edges_from(data)
    Mileage =300
    S_D_dis = nx.dijkstra_path_length(G,sp,fd)
    Dis_des_near_cs = nx.dijkstra_path_length(G,fd,cs)
    Threh = threshold(S_D_dis, charging, Mileage, Dis_des_near_cs)

    if (charging > 60 & Threh == True) :
        path = nx.dijkstra_path(G, sp, fd)

        return path

    elif (charging < 20):

        print("Charge your Vechile")

        return 1

    elif(Threh==False) :
        path_1 = nx.dijkstra_path(G, sp, cs)
        path_2 = nx.dijkstra_path(G, cs, fd)

        path = path_1[0:-1] + path_2

        return path


def plot_graph(dict,path) :

    lat = []
    long = []
    for i in range(len(path)) :
        lat.append(dict[path[i]][0])
        long.append(dict[path[i]][1])

    gmap = gmplot.GoogleMapPlotter(dict[path[i]][0],dict[path[i]][1], 15)

    gmap.scatter(lat, long, 'red', size=50, marker=False)

    gmap.plot(lat, long, 'blue', edge_width=2)

    j = gmap.draw('./templates/graph_to_map.html')

    return j

dict = {'p1':(26.47360920927213, 73.11462854805787) ,
'p2':(26.473056425743557, 73.11440398903673) ,
'p3':(26.472604146335616, 73.11429170952616) ,
'p4':(26.47345845039137, 73.11507766610015) ,
'p5':(26.472955919362118, 73.11490924683429) ,
'p6':(26.47256645630472, 73.114853107079) ,
'p7':(26.47345845039137, 73.11530222512128) ,
'p8':(26.47399238720489, 73.11589169255177) ,
'p9':(26.47403007676868, 73.1161794087976) ,
'p10':(26.473364225990576, 73.11590572749058) ,
'p11':(26.47286169454976, 73.11580046544944) ,
'p12':(26.4724847945287, 73.1157794130412) ,
'p13':(26.474086611091224, 73.11731623884212) ,
'p14':(26.473766249562846, 73.11727413402566) ,
'p15':(26.47370880422433, 73.116877184489) ,
'p16':(26.473237037455238, 73.11674542679347) ,
'p17':(26.47279054212412, 73.11670778173759) ,
'p18':(26.472411440954517, 73.11667013668173) ,
'p19':(26.47407947675721, 73.1177618433019) ,
'p20':(26.472664175206383, 73.11753597296669) ,
'p21':(26.472150281644385, 73.11729128010356)}

data = [('p1' , 'p4' ,45.14) ,('p1' , 'p2' ,64.45) ,('p2' , 'p5' ,50.07) ,
('p2' , 'p3' ,46.33) ,
('p3' , 'p6' ,54.09) ,
('p4' , 'p7' ,27.88) ,
('p4' , 'p5' ,45.89) ,
('p5' , 'p6' ,52.65) ,
('p5' , 'p11' ,85.57) ,
('p6' , 'p12' ,97.02) ,
('p7' , 'p8' ,115.00) ,
('p7' , 'p10' ,68.39) ,
('p8' , 'p10' ,66.20) ,
('p8' , 'p9' ,32.60) ,
('p9' , 'p10' ,77.79) ,
('p9' , 'p13' ,114.85) ,
('p10' , 'p16' ,80.41) ,
('p10' , 'p11' ,55.56) ,
('p11' , 'p12' ,47.89) ,
('p11' , 'p17' ,83.85) ,
('p12' , 'p18' ,79.06) ,
('p13' , 'p14' ,35.38) ,
('p13' , 'p19' ,39.87) ,
('p14' , 'p15' ,41.30) ,
('p15' , 'p16' ,45.97) ,
('p16' , 'p20' ,84.39) ,
('p16' , 'p17' ,54.85) ,
('p17' , 'p21' ,87.92) ,
('p17' , 'p18' ,43.66) ,
('p18' , 'p22' ,98.53) ,
('p19' , 'p20' ,56.70) ,
('p20' , 'p21' ,59.27) ,
('p21' , 'p22' ,74.80)]


# Flask constructor
app = Flask(__name__)   
  
# A decorator used to tell the application
# which URL is associated function

@app.route('/', methods =["GET", "POST"])
def start():
    return render_template('web.html')

@app.route('/map', methods =["GET", "POST"])
def map():
    if request.method == "POST":

       start = request.form.get("cloc")
       end = request.form.get("floc") 
       csata = request.form.get("cstatus")

       pat = shortest_path(str(start),str(end),'p10',int(csata),data)

       a = plot_graph(dict,pat)
        
    return render_template("graph_to_map.html")

# @app.route('/map', methods =["GET", "POST"])
# def map():
#     return render_template('graph_to_map.html')
  
if __name__=='__main__':
    app.run(debug=True)
