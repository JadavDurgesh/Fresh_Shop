from django.shortcuts import render,redirect
from .models import*
import razorpay
from django.conf import settings
from django.core.mail import send_mail
import random


# Create your views here.



def index(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        pid = Add_product.objects.all()
        ctid = Add_to_cart.objects.filter(user_id=uid)
        lid = Add_to_cart.objects.filter(user_id=uid).count()
        con = {
            'uid' : uid,
            'pid' : pid,
            'ctid' : ctid,
            'lid' : lid
        }
        return render(request,"index.html",con)
    else:
        return render(request,"login.html")


def login(request):
    
        if "email" in request.session:
            uid = User.objects.get(email = request.session['email'])
            con = {
                'uid' : uid
            }
            return render(request,"index.html",con)
        else:
                try:
                    if request.POST:
                        
                        email = request.POST['email']
                        password = request.POST['password']
                        
                        uid = User.objects.get(email=email)
                        pid = Add_product.objects.all()
                        ctid = Add_to_cart.objects.all()
                        lid = Add_to_cart.objects.all().count()
                        
                        
                        
                        if uid.password == password:
                            
                    
                            request.session['email'] = uid.email
                            
                            con = {
                                'uid' : uid,
                                'pid' : pid,
                                'ctid' : ctid,
                                'lid' : lid
                            }
                        
                            return render(request,"index.html",con)
                        else:
                            con = {
                                'eid' : "Invalid Password..."
                            }
                            return render(request,"login.html",con)
                    else:
                        return render(request,"login.html")
                except:
                    con = {
                        'eid' : "Invalid Email.."
                    }
                    return render(request,"login.html",con)

def logout(request):
    if "email" in request.session:
        del request.session['email']
        return render(request,"login.html")
    else:    
        return render(request,"logout.html")

def about(request):
    uid = User.objects.get(email = request.session['email'])
    lid = Add_to_cart.objects.filter(user_id=uid).count()
    ctid = Add_to_cart.objects.filter(user_id=uid)
    
    con = {
        'lid' : lid,
        'ctid' : ctid
    }
    return render(request,"about.html",con)

def cart(request):
    uid = User.objects.get(email = request.session['email'])
    
    cid = Add_to_cart.objects.filter(user_id=uid)
    ctid = Add_to_cart.objects.filter(user_id=uid)
    
    lid = Add_to_cart.objects.filter(user_id=uid).count()
    con = {
        'cid' : cid,
        'lid' : lid,
        'ctid' : ctid
    }
    return render(request,"cart.html",con)

def remove(request,id):
    rid = Add_to_cart.objects.get(id=id).delete()
    
    return redirect('cart')

def plus(request,id):
    
    pid = Add_to_cart.objects.get(id=id)
    
    if pid:
        
        pid.qty = pid.qty + 1
        pid.total_price = pid.qty * pid.price
        pid.save()
        
        return redirect('cart')
    
def minus(request,id):
    
    mid = Add_to_cart.objects.get(id=id)
    
    if mid.qty == 1:
        mid.delete()
        return redirect('cart')
    else:
    
        if mid:
            
            mid.qty = mid.qty - 1
            mid.total_price = mid.qty * mid.price
            mid.save()
            
            return redirect('cart')    
        
def remove_wishlist(request,id):
    did = Wishlist.objects.get(id=id).delete()
    
    return redirect('wishlist')
        
        
        
def add_to_wishlist(request,id):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        pid = Add_product.objects.get(id=id)
        
        
        wid = Wishlist.objects.create(user_id=uid,
                                      product_id=pid,
                                      name=pid.name,
                                      pic=pid.pic,
                                      price=pid.price)
        return redirect('wishlist')
    else:
        return render(request,"index.html")        

def checkout(request):
    uid = User.objects.get(email = request.session['email'])
    lid = Add_to_cart.objects.filter(user_id=uid).count()
    ctid = Add_to_cart.objects.filter()
    prod = Add_to_cart.objects.filter(user_id=uid)
    
    list1 = []
    sub_total = 0
    total = 1
    
    try:
        for i in prod:
            z = i.price * i.qty
            list1.append(z)
            a = sum(list1)
        sub_total = sub_total + a
        total = sub_total + 50
        
            
        amount = total*100 
        client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))
        response = client.order.create({

                                        'amount':amount,
                                    'currency':'INR',
                                    'payment_capture':1
        
        })
            
        
        con = {
            'lid' : lid,
            'ctid' : ctid,
            'prod' : prod,
            'response' : response,
            'total' : total,
            'sub_total' : sub_total
        }
        
        for i in prod:
            Order.objects.create(user_id = uid,
                                name = i.name,
                                qty = i.qty,
                                price = i.price)
        
        return render(request,"checkout.html",con)

    except:
        return render(request,"checkout.html")



def order(request):
    uid = User.objects.get(email = request.session['email'])
    oid = Order.objects.filter(user_id=uid)
    aid = Address.objects.filter(user_id=uid)
    did = Add_to_cart.objects.filter(user_id=uid).delete()
    
    con = {
        'oid' : oid,
        'aid' : aid,
    }
    return render(request,"order.html",con)     

def billing_address(request):
    
    try:
    
        uid = User.objects.get(email = request.session['email'])
        lid = Add_to_cart.objects.filter(user_id=uid).count()
        ctid = Add_to_cart.objects.filter()
        aid = Address.objects.filter(user_id=uid).exists()
        add_list = Address.objects.get(user_id=uid)
        
        print(uid,aid,"---------------------")
        if aid:
            lid = Add_to_cart.objects.all()   
            l1 = []
            for i in lid:
                    
                l1.append(f"product name = {i.name} price = {i.price} qty = {i.qty} total_price = {i.total_price}......")
                
                
            add_list.list = l1 
            add_list.save()   
            return redirect('checkout')
    
    except:
    
        if request.POST:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user_name = request.POST['user_name']
            email = request.POST['email']
            address = request.POST['address']
            address_2 = request.POST['address_2']
            country = request.POST['country']
            state = request.POST['state']
            pincode = request.POST['pincode']
            
            uid = Address.objects.create(user_id=uid,
                                        first_name=first_name,
                                        last_name=last_name,
                                        user_name=user_name,
                                        email=email,
                                        address=address,
                                        address_2=address_2,
                                        country=country,
                                        state=state,
                                        pincode=pincode)
            
            lid = Add_to_cart.objects.all()
            
            l1 = []
            for i in lid:
                
                l1.append(f"product name = {i.name} price = {i.price} qty = {i.qty} total_price = {i.total_price}......")
            
            
            uid.list = l1 
            uid.save()   
            return redirect('checkout')

        else:    
            con = {
                'lid' : lid,
                'ctid' : ctid
            }
        
            return render(request,"billing_address.html",con)
        
   
        
def delete_address(request):
    uid = User.objects.get(email = request.session['email'])
    try:
        did = Address.objects.get(user_id=uid).delete()
    
        return redirect('billing_address')    
    except:    
        return render(request,"billing_address.html")
        
        

def contact_us(request):
    uid = User.objects.get(email = request.session['email'])
    
    lid = Add_to_cart.objects.filter(user_id=uid).count()
    ctid = Add_to_cart.objects.filter(user_id=uid)
    
    
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        lid = Add_to_cart.objects.all().count()

        
        uid = Contact_us.objects.create(name=name,
                                        email=email,
                                        subject=subject,
                                        message=message)
        
        con = {
           
            'sid' : "successfully add contact....",
            'lid' : lid
            
        }
    
        return render(request,"contact_us.html",con)
    else:
        con = {
            'lid' : lid,
            'ctid' : ctid
        }
        return render(request,"contact_us.html",con)


def gallery(request):
    uid = User.objects.get(email = request.session['email'])
    lid = Add_to_cart.objects.filter(user_id=uid).count()
    ctid = Add_to_cart.objects.filter(user_id=uid)
    gid = G_categories.objects.all()
    pid = G_subcategories.objects.all()
    
    
    con = {
        'lid' : lid,
        'ctid' : ctid,
        'gid' : gid,
        'pid' : pid
    }
    return render(request,"gallery.html",con)

def g_categories(request,id):
    pid = G_subcategories.objects.filter(c_id=id)
    
    gid = G_categories.objects.all()
    
    con = {
        'pid' : pid,
        'gid' : gid
    }
    return render(request,"gallery.html",con)
    

def my_account(request):
    uid = User.objects.get(email = request.session['email'])
    
    lid = Add_to_cart.objects.filter(user_id=uid).count()
    ctid = Add_to_cart.objects.filter(user_id=uid)
    
    con = {
        'lid' : lid,
        'ctid' : ctid
    
    }
    
    return render(request,"my_account.html",con)

def shop_detail(request,id):
    uid = User.objects.get(email = request.session['email'])
    
    vid = Add_product.objects.get(id=id)
    lid = Add_to_cart.objects.filter(user_id=uid).count()
    ctid = Add_to_cart.objects.filter(user_id=uid)
    
    con = {
        'vid' : vid,
        'lid' : lid,
        'ctid' : ctid
    }
    return render(request,"shop_detail.html",con)

def shop(request):
    uid = User.objects.get(email = request.session['email'])
    
    pid = Add_product.objects.all()
    cid = Categories.objects.all()
    sid = sub_categories.objects.all()
    lid = Add_to_cart.objects.filter(user_id=uid).count()
    ctid = Add_to_cart.objects.filter(user_id=uid)
    low_to_high = request.GET.get('low_to_high')
    high_to_low = request.GET.get('high_to_low')
    A_to_Z =request.GET.get('A_to_Z')
    Z_to_A =request.GET.get('Z_to_A')
    
    
    if low_to_high:
        pid = Add_product.objects.order_by('price')
        
    elif high_to_low:    
        pid = Add_product.objects.order_by('-price')
        
    elif A_to_Z:
        pid = Add_product.objects.order_by('name')
        
    elif Z_to_A:
        pid = Add_product.objects.order_by('-name')        
        
        
    else:
        pid = Add_product.objects.all()
        
    con = {
        'pid' : pid,
        'cid' : cid,
        'lid' : lid,
        'sid' : sid,
        'ctid' : ctid,
        'low_to_high' : low_to_high,
        'A_to_Z' : A_to_Z,
        'Z_to_A' : Z_to_A
    }
    return render(request,"shop.html",con)


def categories(request,id):
    
    pid = Add_product.objects.filter(categories_id=id)
    cid = Categories.objects.all()
    sid = sub_categories.objects.all()
    
    con = {
        'pid' : pid,
        'cid' : cid,
        'sid' : sid
    }
    return render(request,"shop.html",con)
    
def s_categories(request,id):
    
    pid = Add_product.objects.filter(s_id=id)
    sid = sub_categories.objects.all()
    cid = Categories.objects.all()
    
    
    con = {
        'pid' : pid,
        'sid' : sid,
        'cid' : cid
    }
    return render(request,"shop.html",con)


def add_to_cart(request,id):
    
    if "email" in request.session:
            uid = User.objects.get(email = request.session['email'])
            pid = Add_product.objects.get(id=id)
            pcid = Add_to_cart.objects.filter(user_id=uid,product_id=pid).exists()
            
            if pcid:
                pcid = Add_to_cart.objects.get(product_id = pid)
                pcid.qty = pcid.qty + 1
                pcid.total_price = pcid.price * pcid.qty
                pcid.save()
                return redirect('cart')
            else:

            
                aid = Add_to_cart.objects.create(user_id = uid,
                                             product_id = pid,
                                             name = pid.name,
                                             price = pid.price,
                                             qty = pid.qty,
                                             pic = pid.pic,
                                             total_price = pid.qty * pid.price)
                return redirect('cart')        
            
            
    else:
        return render(request,"shop.html")     
    


def wishlist(request):
    uid = User.objects.get(email = request.session['email'])
    
    lid = Add_to_cart.objects.filter(user_id=uid).count()
    ctid = Add_to_cart.objects.filter(user_id=uid)
    wid = Wishlist.objects.all()
    
    con = {
        'lid' : lid,
        'ctid' : ctid,
        'wid' : wid
    }
    
    return render(request,"wishlist.html",con)

def register(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        
        uid = User.objects.create(name=name,
                                  email=email,
                                  password=password)
        return redirect('login')

    
    else:
    
        return render(request,"register.html")

def search(request):
    
    name = request.GET['name']
    
    if name:
        pid = Add_product.objects.filter(name__contains=name)
        
        con = {
            'pid' : pid
        }
        return render(request,"shop.html",con)

    else:
        
        
        return render(request,"index.html")

def forget_password(request):
    
    if request.POST:
        email = request.POST['email']
        otp = random.randint(1111,9999)
        
        try:
            
            uid = User.objects.get(email=email)
            uid.otp = otp
            uid.save()
            
            send_mail("Forget Password","Your OTP is"+str(uid.otp),'gohiljayb10@gmail.com',[email])
            con = {
                'email' : email
            }
            return render(request,"confirm_password.html",con)
            
            
        except:
            pass    
    else:
        return render(request,"forget_password.html")


def confirm_password(request):
    
    if request.POST:
        email = request.POST['email']
        otp = request.POST['otp']
        new_password = request.POST['new_password']
        c_password = request.POST['c_password']
        
        uid = User.objects.get(email=email)
        
        if str(uid.otp) == otp:
            
            if new_password == c_password:
                uid.password = new_password
                uid.save()
                con = {
                    'uid' :uid
                }   
                return render(request,"login.html",con)           
                
            else:    
                return render(request,"confirm_password.html")   
    else:
        
        return render(request,"confirm_password.html")    
        
    
def change_password(request):
    
    uid = User.objects.get(email = request.session['email'])
    
    if request.POST:
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        if uid.password == current_password:
            if new_password == confirm_password:
                uid.password = new_password
                uid.save()
                
                return render(request,"my_account.html")
            
            else:
                con = {
                    'eid' : "Invalid New Password and Confirm Password"
                }
                return render(request,"change_password.html",con)
        else:
            con = {
                    'eid' : "Invalid Current Password"
                }
            return render(request,"change_password.html",con)
    else:
            return render(request,"change_password.html")    
        
                    
                
                
                
        
    