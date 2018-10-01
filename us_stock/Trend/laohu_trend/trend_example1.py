from scipy.optimize import minimize, bracket, minimize_scalar


def f(x):
	return (x-1)*(x+5)*(x-3)*(x+10)

# res = minimize_scalar(f,  bounds=(-3, 60000000000),  method='bounded')

#局域最低点


res1 = bracket(f, xa = 5, xb=4)
print(res1)
res = minimize_scalar(f,  bounds=(res1[2],res1[1]),  method='bounded')
print(res.x)




