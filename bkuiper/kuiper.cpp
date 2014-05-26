// ########################################################################
// #   Kuiper's statistic C (for python import) library
// #    Copyright (C) 2014  Bruno Ribeiro
// #
// #    This program is free software: you can redistribute it and/or modify
// #    it under the terms of the GNU General Public License as published by
// #    the Free Software Foundation, either version 3 of the License, or
// #    (at your option) any later version.
// #
// #    This program is distributed in the hope that it will be useful,
// #    but WITHOUT ANY WARRANTY; without even the implied warranty of
// #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// #    GNU General Public License for more details.
// #
// #    You should have received a copy of the GNU General Public License
// #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
// ########################################################################


#include <cmath>
#include <iostream>
#include <algorithm>

using namespace std;

//
// From Chapter 14.3.4 of Numerical Recipes
//

class Kuiper{
    public:
      double qKP(double lambda) {
        int j;
        long double kp_sum;
        
        kp_sum = 0.0;
        for (j=1; j < 1000; j++) {
           kp_sum += (4.0 * j*j * lambda * lambda - 1) * exp(-2.0 * j*j*lambda*lambda);
        }
        return ((double)(2.0*kp_sum));
      }


      double kptwo(double* data1, double* data2, int n1, int n2)
      // Given an array data1[0..n1-1], and an array data2[0..n2-1], this routine returns the K–S statistic d and the p-value prob for the null hypothesis that the data sets are drawn from the same distribution. Small values of prob show that the cumulative distribution function of data1 is significantly different from that of data2. The arrays data1 and data2 are modified by being sorted into ascending order.
      {
          int j1=0,j2=0;
          double Dmin,Dplus,V;
          double d1,d2,en1,en2,en,fn1=0.0,fn2=0.0;
          sort(data1,data1+n1);
          sort(data2,data2+n2);
          en1=(double)n1;
          en2=(double)n2;
          Dplus=0.0;
          Dmin=0.0;
          V=0.0;
          while (j1 < n1 && j2 < n2) {
              if ((d1=data1[j1]) <= (d2=data2[j2])) {
                 do {
                     fn1=++j1/en1;
                 } while (j1 < n1 && d1 == data1[j1]);
              }
              if (d2 <= d1)
              {
                 do {
                     fn2=++j2/en2;
                 } while (j2 < n2 && d2 == data2[j2]);
              }
              if (Dplus < fn2-fn1) {
                 Dplus = fn2-fn1;
              }
              if (Dmin < fn1-fn2) {
                  Dmin = fn1-fn2;
              }
          }
          en=sqrt(en1*en2/(en1+en2));
          V = Dmin + Dplus;
          return(qKP((en+0.155+0.24/en)*V));
      }
  
      void initkuiper()
      {
      }

};

extern "C" {
    Kuiper* Kuiper_new(){ return new Kuiper(); }
    void initkuiper() { initkuiper(); }
    double Kuiper_kptwo(Kuiper* kuiper,double* data1, double* data2, int n1, int n2){ return (kuiper->kptwo(data1, data2, n1, n2)); }
}
