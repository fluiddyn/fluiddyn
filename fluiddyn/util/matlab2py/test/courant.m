% Set the upper bound on dt:
% Sometimes this is useful when starting with very small perturbations,

% First, set a time-step constraint based on diffusion
dt=0.5*min(min(min(DX(ii,jj),DY(ii,jj))))/(1/Re);
for n=1:N_TH
  dt=min(dt,dt*(1/Re)/(1/Re/PR(n))); % Take the larger of nu and kappa
end
% Make sure that we capture the inertial period (for rotating flows)
if (I_RO~=0)
  dt=min(dt,2*pi/I_RO/20);
end
% Make sure that we capture the buoyancy period (for stratified flows)
for n=1:N_TH
  if (RI(n)~=0)
    dt=min(dt,0.25*2*pi/Nmax);
  end
end


% Now, enforce the CFL critiria
dt_y=CFL*min(min(DY(3:NX-1,3:NY-1)./abs(U2(3:NX-1,3:NY-1))));  % Avoid j=2 which is a ghost cell

if (dt<=0)  error('DT<=0 in courant'); end;

% Set the size of the timestep (DELTA_T), and the RK substeps (H_BAR)
DELTA_T=dt;


