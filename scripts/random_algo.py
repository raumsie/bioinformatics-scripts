import math
import random

def f(x, A, B, k, p):
    """
    Calculate the value of the equation: A*x^k + B*x^p + tan(A*x^k + B*x^p)
    """
    term1 = A * (x ** k)
    term2 = B * (x ** p)
    inner = term1 + term2
    return inner + math.tan(inner)

def find_root_monte_carlo(A, B, k, p, max_iterations=10000, tolerance=1e-10):
    """
    Find a root of the equation using Monte Carlo approach
    """
    print(f"Searching for root of equation with A={A}, B={B}, k={k}, p={p}")
    print(f"Equation: {A}*x^{k} + {B}*x^{p} + tan({A}*x^{k} + {B}*x^{p}) = 0")
    
    # Step 1: Find initial bracket [x1, x2] where f(x1) > 0 and f(x2) < 0
    x1, x2 = None, None
    search_range = 100  # Start with a wide search range
    
    print("\nStep 1: Finding initial bracket...")
    for i in range(max_iterations // 2):
        x = random.uniform(-search_range, search_range)
        
        try:
            fx = f(x, A, B, k, p)
            
            if x1 is None and fx > 0:
                x1 = x
                print(f"Found x1 = {x:.6f}, f(x1) = {fx:.6f} > 0")
            
            if x2 is None and fx < 0:
                x2 = x
                print(f"Found x2 = {x:.6f}, f(x2) = {fx:.6f} < 0")
            
            if x1 is not None and x2 is not None:
                break
                
        except (ValueError, OverflowError):
            # Handle cases where tan might be undefined or calculation overflows
            continue
    
    if x1 is None or x2 is None:
        print("Could not find initial bracket. Trying alternative approach...")
        # Alternative: look for any two points with opposite signs
        for i in range(1000):
            xa = random.uniform(-search_range, search_range)
            xb = random.uniform(-search_range, search_range)
            
            try:
                fa = f(xa, A, B, k, p)
                fb = f(xb, A, B, k, p)
                
                if fa * fb < 0:  # Opposite signs
                    if fa > 0:
                        x1, x2 = xa, xb
                    else:
                        x1, x2 = xb, xa
                    break
            except (ValueError, OverflowError):
                continue
    
    if x1 is None or x2 is None:
        return None, [], float('inf')
    
    print(f"\nInitial bracket: x1 = {x1:.6f}, x2 = {x2:.6f}")
    print(f"f(x1) = {f(x1, A, B, k, p):.6f}, f(x2) = {f(x2, A, B, k, p):.6f}")
    
    # Step 2: Refine the solution
    trace = []
    best_x = (x1 + x2) / 2
    best_fx = abs(f(best_x, A, B, k, p))
    
    print("\nStep 2: Refining solution...")
    for i in range(max_iterations // 2):
        # Randomly select a point between x1 and x2
        x_new = random.uniform(min(x1, x2), max(x1, x2))
        
        try:
            fx_new = f(x_new, A, B, k, p)
            
            # Update the bracket
            if fx_new > 0:
                x1 = x_new
            elif fx_new < 0:
                x2 = x_new
            
            # Keep track of best solution
            if abs(fx_new) < best_fx:
                best_x = x_new
                best_fx = abs(fx_new)
            
            # Record trace
            trace.append((x1, x2, x_new, fx_new))
            
            # Check for convergence
            if abs(fx_new) < tolerance:
                print(f"Converged after {i+1} iterations")
                break
                
            # If bracket is too small, we're done
            if abs(x1 - x2) < 1e-15:
                break
                
        except (ValueError, OverflowError):
            continue
    
    return best_x, trace, best_fx

def main():
    # Test cases
    test_cases = [
        (1, 1, 1, 1),    # Simple case: x + x + tan(2x) = 2x + tan(2x) = 0
        (1, -1, 2, 1),   # x^2 - x + tan(x^2 - x) = 0
        (2, 3, 1, 1),    # 2x + 3x + tan(5x) = 5x + tan(5x) = 0
        (1, 0, 2, 0),    # x^2 + tan(x^2) = 0
    ]
    
    results = []
    
    for i, (A, B, k, p) in enumerate(test_cases):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i+1}")
        print(f"{'='*60}")
        
        x, trace, error = find_root_monte_carlo(A, B, k, p, max_iterations=5000)
        
        if x is not None:
            print(f"\nRESULT for Test Case {i+1}:")
            print(f"Found x = {x:.10f}")
            print(f"f(x) = {f(x, A, B, k, p):.10f}")
            print(f"Error = {error:.10f}")
            
            # Show some trace examples
            print(f"\nTrace (first 5 and last 5 iterations):")
            if len(trace) > 10:
                for t in trace[:5]:
                    print(f"  x1={t[0]:.6f}, x2={t[1]:.6f}, x_guess={t[2]:.6f}, f(x)={t[3]:.6f}")
                print("  ...")
                for t in trace[-5:]:
                    print(f"  x1={t[0]:.6f}, x2={t[1]:.6f}, x_guess={t[2]:.6f}, f(x)={t[3]:.6f}")
            else:
                for t in trace:
                    print(f"  x1={t[0]:.6f}, x2={t[1]:.6f}, x_guess={t[2]:.6f}, f(x)={t[3]:.6f}")
        else:
            print("No solution found within the given iterations")
        
        results.append({
            'test_case': f"A={A}, B={B}, k={k}, p={p}",
            'x': x,
            'f(x)': f(x, A, B, k, p) if x is not None else None,
            'error': error
        })
    
    # Write results to file
    with open('results.txt', 'w') as f:
        f.write("Randomized Algorithms Lab Results\n")
        f.write("=" * 50 + "\n\n")
        
        for i, result in enumerate(results):
            f.write(f"Test Case {i+1}: {result['test_case']}\n")
            if result['x'] is not None:
                f.write(f"  x = {result['x']:.10f}\n")
                f.write(f"  f(x) = {result['f(x)']:.10f}\n")
                f.write(f"  |f(x)| = {result['error']:.10f}\n")
            else:
                f.write("  No solution found\n")
            f.write("\n")

if __name__ == "__main__":
    main()

'''
import random
import math

# (Ax^k) + (Bx^p) + tan(Ax^k + Bx^p) = 0
A = int(input('A:'))
B = int(input('B:'))
k = int(input('k:'))
p = int(input('p:'))
print(f'{A}x^({k}) + {B}x^({p}) + tan({A}x^({k}) + {B}x^({p}) = 0')

print('=' * 40)
x = int()


Ax_to_the_k = A * pow(x, k)

Bx_to_the_p = B * pow(x, p)

tan_exp = math.tan(Ax_to_the_k + Bx_to_the_p)

equation = Ax_to_the_k + Bx_to_the_p + tan_exp

def check_if_zero(A, B, k, p, x):
    found = False
    closest_dist = float('inf')
    closest_index = -1
    t = 0
    while
    '''