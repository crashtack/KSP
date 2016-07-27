#include <math.h>
#include <iostream>
#include <cstdlib>

using namespace std;

void bi_elliptical_delta_v (double current_orbit, double bi_elliptical_apoapsis, double final_orbit, double standard_gravitational_parameter, double planet_radius)
{
  double delta_v_1, delta_v_2, delta_v_3, delta_v_total;
  delta_v_1 = sqrt (((2*standard_gravitational_parameter)/current_orbit)-((2*standard_gravitational_parameter)/(current_orbit + bi_elliptical_apoapsis))) - sqrt (standard_gravitational_parameter/current_orbit);
  delta_v_2 = sqrt (((2*standard_gravitational_parameter)/bi_elliptical_apoapsis)-((2*standard_gravitational_parameter)/(final_orbit + bi_elliptical_apoapsis))) - sqrt (((2*standard_gravitational_parameter)/bi_elliptical_apoapsis)-((2*standard_gravitational_parameter)/(current_orbit + bi_elliptical_apoapsis)));
  delta_v_3 = sqrt (((2*standard_gravitational_parameter)/final_orbit)-((2*standard_gravitational_parameter)/(final_orbit + bi_elliptical_apoapsis))) - sqrt (standard_gravitational_parameter/final_orbit);
  delta_v_total = delta_v_1 + delta_v_2 + delta_v_3;
  string fore;
  if (current_orbit < final_orbit)
  {
    fore = "prograde";
  }
  else if (current_orbit > final_orbit)
  {
    fore = "retrograde";
  }
  cout << "Bi-elliptcal transfer stats:" << endl << "Bi-elliptical apoapsis: " << bi_elliptical_apoapsis - planet_radius << "m above sea level" << endl << "Burn 1 = " << delta_v_1 << "m/s prograde" << endl << "Burn 2: " << delta_v_2 << "m/s " << fore << endl << "Burn 3 = " << delta_v_3 << "m/s retrograde" << endl << "Total delta v: " << delta_v_total << "m/s" << endl;
}

void hohmann_delta_v (double current_orbit, double final_orbit, double standard_gravitational_parameter)
{
  double delta_v_1, delta_v_2, delta_v_total;
  delta_v_1 = sqrt (((2*standard_gravitational_parameter)/current_orbit)-((2*standard_gravitational_parameter)/(current_orbit + final_orbit))) - sqrt (standard_gravitational_parameter/current_orbit);
  delta_v_2 = sqrt (((standard_gravitational_parameter)/final_orbit)) - sqrt (((2*standard_gravitational_parameter)/final_orbit)-((2*standard_gravitational_parameter)/(current_orbit + final_orbit)));
  delta_v_total = delta_v_1 + delta_v_2;
  string fore;
  if (current_orbit < final_orbit)
  {
    fore = "prograde";
  }
  else if (current_orbit > final_orbit)
  {
    fore = "retrograde";
  }
  cout << "Hohmann transfer stats:" << endl << "Burn 1 = " << delta_v_1 << "m/s " << fore << endl << "Burn 2: " << delta_v_2 << "m/s " << fore << endl  << "Total delta v: " << delta_v_total << "m/s" << endl;
}

int main ()
{
  cout << "Orbital transfer calculator v2.0\nWritten by TomPN\n18/01/2016\n" << endl;
  double planet_mass;
  cout << "Please enter the mass of the body you are in orbit around (in kilograms x10^20): ";
  cin >> planet_mass;
  double mass_multiplier = 100000000000000000000.0;
  planet_mass *= mass_multiplier;
  double standard_gravitational_parameter = planet_mass*0.0000000000667;
  double planet_radius;
  cout << "Please enter the radius of the body you are in orbit around (in metres): ";
  cin >> planet_radius;
  double current_orbit;
  cout << "Please enter your current orbital altitude above sea level (in metres): ";
  cin >> current_orbit;
  current_orbit += planet_radius;
  double final_orbit;
  cout << "Please enter your desired orbital altitude above sea level (in metres): ";
  cin >> final_orbit;
  final_orbit += planet_radius;
  double sphere_of_influence;
  cout << "Please enter the radius of the sphere of influence of the body that you are\n currently in orbit around (in metres): ";
  cin >> sphere_of_influence;
  cout << endl;
  double bi_elliptical_apoapsis = (0.9*(sphere_of_influence - final_orbit)) + final_orbit;
  hohmann_delta_v (current_orbit, final_orbit, standard_gravitational_parameter);
  cout << endl;
  bi_elliptical_delta_v (current_orbit, bi_elliptical_apoapsis, final_orbit, standard_gravitational_parameter, planet_radius);
  cout << endl;
  system ("PAUSE");
  return 0;
}
