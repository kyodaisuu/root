#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Newton's method
# https://github.com/kyodaisuu/root
# written by Fish
#
# When environmental variable SCRIPT_NAME is set, it runs as a CGI program.
# Otherwise it runs as a commandline program.


def main():
    """Calculate n-th root by Newton's method

    Determine if it is commandline or CGI.
    """
    import os
    if os.getenv('SCRIPT_NAME') is None:
        maincl()
    else:
        maincgi()
    return


def maincl():
    """Calculate n-th root by Newton's method

    Invoked from command line.
    """
    showprocess = True  # When it is False process is not shown.
    p = 40  # precision
    # Test some values
    assert root(4, 2, 20, False) == '2.00000000000000000000'
    assert root(2, 2, 30, False) == '1.414213562373095048801688724209'
    assert root(27, 3, 20, False) == '3.00000000000000000000'
    a = input('Input a number = ')
    assert a > 0, "a should be positive"
    n = 2
    assert n == int(n), "n should be integer"
    assert n > 0, "n should be positive"
    # Calculate square root of a and show the result
    print("{0}-th root of {1} = {2}".format(n, a, root(a, n, p, showprocess)))
    return


def maincgi():
    """Calculate n-th root by Newton's method

    Running as a CGI program.
    """
    import cgi
    # Comment out for debugging
    import cgitb
    cgitb.enable()
    maxprec = 10000
    # Get form input
    f = cgi.FieldStorage()
    a = f.getfirst('a', '')
    n = f.getfirst('n', '')
    p = f.getfirst('p', '')
    if n.isdigit() == False:
        n = 2
    if p.isdigit() == False or int(p) < 5:
        p = 20
    if p.isdigit() and int(p) > maxprec:
        p = maxprec
    # Write html
    print(r'''Content-Type: text/html

<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>n乗根の計算</title>
  <link rel="stylesheet" type="text/css" href="fish.css">
</head>
<body>
<h1>n乗根の計算</h1>

<form action="root.cgi" method="post">
  <input type="text" name="a" value="{0}"/> の <input type="text" name="n" size="5" value="{1}" /> 乗根の計算<br>
  桁数 <input type="text" name="p" size="5" value="{2}" />
  <input type="submit" />
</form>
'''.format(a, n, p))
    # Calculate n-th root of a
    if isfloat(a) and float(a) >= 0 and int(n) > 0 and int(p) > 1:
        a = float(a)
        if int(a) == a:
            a = int(a)
        n = int(n)
        p = int(p)
        print("<h2>ニュートン法の計算過程</h2><pre>")
        result = root(a, n, p, True)
        print("</pre>\n<h2>結果</h2>")
        print("<p>{0} の {1} 乗根は</p>".format(a, n))
        print("{0}".format(result))
    else:
        print("<p>任意精度でn乗根を計算します。ニュートン法の計算過程も表示します。</p>")
    print(r'''<hr>
<p style="text-align: right;"><a
href="https://github.com/kyodaisuu/root">n乗根</a></p>
</body>
</html>
''')
    return


def root(a, n, p, showprocess):
    """Calculate n-th root of a with precision of p

    When showprocess = True, calculation process is shown.
    """
    aint = int(int(a * 10**15) * 10 ** (p*n-15))
    prev = (int((a+1) ** (1.0/n))+1) * 10 ** p
    if showprocess:
        print(num(prev, p))
    while True:
        x = (prev * (n-1) + aint // (prev ** (n-1))) // n
        if showprocess:
            print(num(x, p))
        if abs(x - prev) < 10:
            break
        prev = x
    return num(x, p)


def num(a, p):
    """Return a / 10^p"""
    a = int(a)
    m = str(a % 10**p)
    m = '0'*(p-len(m))+m
    return str(a // 10**p) + "." + m


def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    main()
