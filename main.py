import os
from datetime import datetime
import base64
from tabnanny import check
from click import DateTime
from flask import Flask, flash, render_template, request, escape
from werkzeug.utils import secure_filename
from DBcm import UseDatabase


UPLOAD_FOLDER = 'static/imglogo'


app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'sportlogo',
                          'password': 'sportlogo',
                          'database': 'sportlogo', }


class CoastItemLayer:
    def __init__(self, id, name, desc, img) -> None:
        self.id=id
        self.name=name
        self.desc=desc
        self.img=img
    @staticmethod
    def add_coast_of_product_header_table(req: 'flask_request'):
        f = request.files['File']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #"File saved successfully"
        emblema=os.path.join(app.config['UPLOAD_FOLDER'])+'/'+filename
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """INSERT INTO product_price_name
                    (name, description, image)
                    VALUES
                    (%s, %s, %s)"""
            cursor.execute(_SQL, (req.form['new_item_name'],                                                            
                                req.form['new_coast_item_desc'],
                                emblema
                                ))
    @staticmethod
    def readCoastProductCategory(req: 'flask_request'):
        with UseDatabase(app.config['dbconfig']) as cursor:        
            cursor.execute("SELECT id, name, description, image FROM product_price_name")
            return cursor.fetchall()
    @staticmethod
    def editCoastProductCategory(req: 'flask_request'):
        with UseDatabase(app.config['dbconfig']) as cursor:        
            id=(req.form['item_header_id'])
            name=(req.form['new_item_name'])
            desc=(req.form['new_coast_item_desc'])
            #set_name="set name "
            #set_definitions="set definitions "
            #where=" where id="
            _SQL="""UPDATE product_price_name 
                    SET name =%s                
                    WHERE id=%s"""
            #_SQL=_SQL+strval
            data=(name,id)
            cursor.execute(_SQL,data)
            _SQL="""UPDATE product_price_name                 
                    SET definitions=%s
                    WHERE id=%s"""
            data=(desc,id)
            cursor.execute(_SQL,data)
    @staticmethod
    def removeCoastProductCategory(req: 'flask_request'):
        with UseDatabase(app.config['dbconfig']) as cursor:        
            id=(req.form['item_header_id'])
            _SQL="""DELETE FROM product_price_name
                WHERE id=            
            """
            #_SQL=_SQL+strval
            cursor.execute(_SQL+id)


class CoastItem:
    def __init__(self, id, id_layer, name, size, coast) -> None:
        self.id=id
        self.id_layer=id_layer        
        self.name=name
        self.size=size
        self.coast=coast   
    @staticmethod
    def writeCoastProductItem(req: 'flask_request'):
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """INSERT INTO product_price_coast
                    (name_id, size, coast)
                    VALUES
                    (%s, %s, %s)"""
            cursor.execute(_SQL, (req.form['item_name'],                                                            
                                req.form['new_item_size_one'],
                                req.form['new_item_coast_one'],                              
                                ))
    @staticmethod
    def readCoastProductItem(req: 'flask_request'):
        pass
    @staticmethod
    def editCoastProductItem(req: 'flask_request'):
        with UseDatabase(app.config['dbconfig']) as cursor:
            id=(req.form['edit_id'])
            size=(req.form['new_item_size_one'])
            coast=(req.form['new_item_coast_one'])
            _SQL = """UPDATE product_price_coast                 
                    SET size=%s
                    WHERE id=%s"""        
            data=(size,id)
            cursor.execute(_SQL,data)
            _SQL="""UPDATE product_price_coast
                    SET coast=%s
                    WHERE id=%s"""
            data=(coast,id)
            cursor.execute(_SQL,data)
    @staticmethod
    def removeCoastProductItem(req: 'flask_request'):
        with UseDatabase(app.config['dbconfig']) as cursor:        
            id=(req.form['remove_id'])
            _SQL="""DELETE from product_price_coast
                    WHERE id=            
            """
            #_SQL=_SQL+id
            cursor.execute(_SQL+id)
                          

@app.route('/')
@app.route('/index')
def index() -> 'html':
    list_pricing_item=[]
    list_pricing_item_layer=[]    
    with UseDatabase(app.config['dbconfig']) as cursor:        
        product_name = CoastItemLayer.readCoastProductCategory(request)    
        for row in product_name:
            list_pricing_item_layer.append(CoastItemLayer(row[0],row[1],row[2],row[3])) 
        #cursor.execute("""select id, id_name, size, coast
        #                    from pricing
        #                    ;""")
        cursor.execute("""SELECT i.id, i.name_id, h.name, i.size, i.coast
                            FROM product_price_name h INNER JOIN product_price_coast i 
                            ON h.id=i.name_id;""")        
        #cursor.execute("""select h.id, h.name, i.id_name, i.size, i.coast 
        #                    from pricing_name h inner join pricing i 
        #                    on h.id=i.id_name 
        #                    where h.name='Эмблемы в оригинале';""")        
        product_size_coast = cursor.fetchall()        
        for row in product_size_coast:
            list_pricing_item.append(CoastItem(row[0],row[1],row[2],row[3],row[4])) 
        
    return render_template('index.html',
                                list_pricing_item_layer=list_pricing_item_layer,
                                list_pricing_item=list_pricing_item                                                  
                            )



@app.route('/dashbrd')
def dashbrd() -> 'html':    
    return render_template('dashbrd.html')


@app.route('/add_new_coast_item_header', methods=['POST', 'GET'])
def add_new_item_coast_header() -> 'html': 
    if request.method == 'POST':
        if request.form['add_new_item'] == 'Добавить':
            CoastItemLayer.add_coast_of_product_header_table(request)            
            # Upload list_item_layer                        
            result_db = CoastItemLayer.readCoastProductCategory(request)
            list_pricing_item_layer=[]
            for row in result_db:
                list_pricing_item_layer.append(CoastItemLayer(row[0], row[1], row[2], row[3]))        
            ###########
            return render_template('dashbrd_coast_edit.html'
                            )

@app.route('/add_new_coast_item', methods=['POST', 'GET'])
def add_new_item_coast() -> 'html':
    if request.method == 'POST':
        if request.form['add_new_item'] == 'Добавить':
            name_i=request.form['item_name']
            size_i=request.form['new_item_size_one']
            coast_i=request.form['new_item_coast_one']
            CoastItem.writeCoastProductItem(request)                        
            return render_template('dashbrd_coast_edit_desc.html',                                    
                            )

@app.route('/edit_new_coast_item', methods=['POST', 'GET'])
def edit_new_item_coast() -> 'html':
    if request.method == 'POST':
        if request.form['edit_old_item'] == 'Изменить':
            name_i=request.form['edit_id']
            size_i=request.form['new_item_size_one']
            coast_i=request.form['new_item_coast_one']
            CoastItem.editCoastProductItem(request)            
            return render_template('test_admin.html',
                                    title="edit old",
                                    name=name_i,
                                    size=size_i,
                                    coast=coast_i
            )

@app.route('/remove_new_coast_item', methods=['POST'])
def reove() -> 'html':    
    if request.method == 'POST':       
        CoastItem.removeCoastProductItem(request)
        #remove_coast_of_product(request)
        return render_template('dashbrd_coast_edit_desc.html')


@app.route('/dashbrd_coast_edit')
def dashbrd_coast_edit() -> 'html':   
    list_pricing_item_layer=[]    
    list_pricing_item=[]
    with UseDatabase(app.config['dbconfig']) as cursor:        
        #cursor.execute("select id, name, definitions, image from pricing_name")
        #result_db = cursor.fetchall()        
        result_db=CoastItemLayer.readCoastProductCategory(request)        
        for row in result_db:
            list_pricing_item_layer.append(CoastItemLayer(row[0], row[1], row[2],row[3]))
        cursor.execute("""SELECT i.id, i.name_id, h.name, i.size, i.coast 
                            FROM product_price_name h INNER JOIN product_price_coast i 
                            ON h.id=i.name_id;""")        
        result_db = cursor.fetchall()        
        for row in result_db:
            list_pricing_item.append(CoastItem(row[0],row[1],row[2],row[3],row[4]))
        return render_template('dashbrd_coast_edit.html',      
                            list_pricing_item_layer=list_pricing_item_layer,      
                            list_pricing_item=list_pricing_item
                            )

@app.route('/dashbrd_coast_edit_desc')
def dashbrd_coast_edit_desc() -> 'html':   
    list_pricing_item_layer=[]
    list_pricing_item=[]
    with UseDatabase(app.config['dbconfig']) as cursor:        
        cursor.execute("SELECT id, name, description, image FROM product_price_name")
        result_db = cursor.fetchall()        
        for row in result_db:
            list_pricing_item_layer.append(CoastItemLayer(row[0], row[1], row[2], row[3]))
        cursor.execute("""SELECT i.id, i.name_id, h.name, i.size, i.coast 
                            FROM product_price_name h INNER JOIN product_price_coast i 
                            ON h.id=i.name_id;""")        
        result_db = cursor.fetchall()        
        for row in result_db:
            list_pricing_item.append(CoastItem(row[0],row[1],row[2],row[3],row[4]))
        return render_template('dashbrd_coast_edit_desc.html',            
                            list_pricing_item_layer=list_pricing_item_layer,
                            list_pricing_item=list_pricing_item
                            )

@app.route('/delete_new_coast_item_header', methods=['POST'])
def delete_new_coast_item_header() -> 'html':    
    if request.method == 'POST':        
        CoastItemLayer.removeCoastProductCategory(request)
        #delete_header_name(request)
        return render_template('dashbrd_coast_edit_desc.html')

@app.route('/edit_new_coast_item_header', methods=['POST'])
def edit_new_coast_item_header() -> 'html':    
    if request.method == 'POST':        
        CoastItemLayer.editCoastProductCategory(request)
        #edit_header_name(request)
        return render_template('dashbrd_coast_edit_desc.html')


if __name__ == '__main__':
    app.run(debug=True)