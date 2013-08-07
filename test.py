a = [1, 2, 3]
b= [4, 5, 6]
x = [ a, b]

print x

def test_modify_list_value(mylist):
    mylist[0] = 100

## cannot reassign ref of incoming parameter
def test_modify_list_ref(mylist):
    mylist = ['evil',]

test_modify_list_value(a)
print a

test_modify_list_value(a)
print a

def test_modify_matrix_value(matrix):
    matrix[0][1]= 'boo'

test_modify_matrix_value(x)
print x

def test_modify_matrix_list(matrix):
    matrix[0] = b

test_modify_matrix_list(x)
print x
