import sklearn
from sklearn import linear_model
from sklearn import svm
import numpy as np

#from stats.models import ConditionInstanceFit, SeriesStableStats, SeriesStartupStats
#from system.models import Condition, ConditionInstance
#from data.models import Run, Apparatus, Diagnostic

def fit_linear_model(dg,model_type="Lasso", alpha=0.01):
    # Query for all runs with input params & with particular diagnostic stat
    headers = ["Arc Current (A)", "Plasma gas (g/s)", "arc_length (m)", "nozzle_diameter (m)"]
    app = Apparatus.objects.filter(name = "mini-ARC v2.0").first()
    runs = Run.objects.filter(test__apparatus = app, diagnostics__in=[dg]).distinct()
    current = Diagnostic.objects.filter(name="Arc Current [A]").first()
    mfr = Diagnostic.objects.filter(name="Plasma gas [g/s]").first()
    
    # Parse and shape data (each row is a sample point)
    samples,output = [],[]
    for run in runs:
        print(run.name)
        arc_length = run.disks.count()*.01 #m
        nozzle_diameter = run.nozzle.diameter/100.
        for ci in run.conditioninstance_set.all():
            if hasattr(ci,'conditioninstancefit'):
                cif = ci.conditioninstancefit
                I_avg = SeriesStableStats.objects.get(condition=cif, series__diagnostic=current).avg
                F_avg = SeriesStableStats.objects.get(condition=cif, series__diagnostic=mfr).avg
                dg_avg = SeriesStableStats.objects.get(condition=cif, series__diagnostic=dg).avg
                samples.append([I_avg, F_avg, arc_length, nozzle_diameter])
                output.append(dg_avg)
    samples = np.array(samples)
    output = np.array(output)

    if model_type == "Lasso":
        reg = linear_model.Lasso(alpha=alpha)
    elif model_type == "Ridge":
        reg = linear_model.Ridge(alpha=alpha)
    
    reg.fit(samples,output)
    return reg.coef_, reg.intercept_

if __name__ == "__main__":
    import os
    import sys
    import django

    proj_path = "/Users/mhaw/Desktop/mARC-db"
    sys.path.append(proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mARC.settings")
    django.setup()

    from system.models import Condition, ConditionInstance
    from stats.models import ConditionInstanceFit, SeriesStableStats, SeriesStartupStats, LinearModel
    from data.models import Run, Apparatus, Diagnostic

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    app = Apparatus.objects.filter(name = "mini-ARC v2.0").first()
    runs = Run.objects.filter(test__apparatus = app)
    current = Diagnostic.objects.filter(name="Arc Current [A]").first()
    mfr = Diagnostic.objects.filter(name="Plasma gas [g/s]").first()
    volts = Diagnostic.objects.filter(name="Arc Voltage [V]").first()
    colpres = Diagnostic.objects.filter(name="Column Pressure [Pa]").first()
    dg = colpres

    # Query for all runs with input params & with particular diagnostic stat
    runs = runs.filter(diagnostics__in=[dg]).distinct()
    
    # Parse and shape data (each row is a sample point)
    samples,output = [],[]
    for run in runs:
        #print(run.name)
        headers = ["Arc Current (A)", "Plasma gas (g/s)", "arc_length (m)", "nozzle_diameter (m)"]
        arc_length = run.disks.count()*.01 #m
        nozzle_diameter = run.nozzle.diameter/100.
        for ci in run.conditioninstance_set.all():
            if hasattr(ci,'conditioninstancefit'):
                try:
                    cif = ci.conditioninstancefit
                    I_avg = SeriesStableStats.objects.get(condition=cif, series__diagnostic=current).avg
                    F_avg = SeriesStableStats.objects.get(condition=cif, series__diagnostic=mfr).avg
                    dg_avg = SeriesStableStats.objects.get(condition=cif, series__diagnostic=dg).avg
                    samples.append([I_avg, F_avg])#, arc_length, nozzle_diameter])
                    output.append(dg_avg)
                except:
                    print("Insufficient data for: ",ci.run.name, ci.run.test.name)
    samples = np.array(samples)
    output = np.array(output)
    x,y = samples[:,0], samples[:,1]


    x_pred = np.linspace(40, 200, 20)   # range of current values
    y_pred = np.linspace(0, .85, 20)  # range of mass flow rate values
    xx_pred, yy_pred = np.meshgrid(x_pred, y_pred)
    model_viz = np.array([xx_pred.flatten(), yy_pred.flatten()]).T

    # Ridge regression model
    reg = linear_model.Ridge(alpha=.01)
    reg.fit(samples,output)
    print(reg.coef_, reg.intercept_)
    print(reg.predict([[160,.25]]))#,0,0]]))
    print(reg.score(samples, output))
    pred = reg.predict(samples)
    predicted = reg.predict(model_viz)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, pred, color='k', zorder=15, linestyle='none', marker='o', alpha=0.5)
    ax.scatter(xx_pred.flatten(), yy_pred.flatten(), predicted, facecolor=(0,0,0,0), s=20, edgecolor='#70b3f0')
    ax.set_xlabel('Current [A]', fontsize=12)
    ax.set_ylabel('Mass flow [g/s]', fontsize=12)
    ax.set_zlabel(dg.name, fontsize=12)


    reg = linear_model.Lasso(alpha=.01)
    reg.fit(samples,output)
    print(reg.coef_, reg.intercept_)
    print(reg.predict([[160,.25]]))
    print(reg.score(samples, output))
    # pred = reg.predict(samples)
    # ax2 = fig.add_subplot(132, projection='3d')

    # reg = linear_model.ElasticNet(alpha=.01, l1_ratio=0.7)
    # reg.fit(samples,output)
    # print(reg.coef_, reg.intercept_)
    # print(reg.predict([[160,.25]]))
    # print(reg.score(samples, output))
    # pred = reg.predict(samples)
    # ax3 = fig.add_subplot(133, projection='3d')

    lm= LinearModel(name=dg.name, diagnostic=dg, coeff=reg.coef_, intercept=reg.intercept_, 
                    headers= ["Arc Current (A)", "Plasma gas (g/s)"], fit_method="Lasso", notes="first")
    #lm.save()

    plt.show()
    # reg = svm.SVR(kernel='poly', C=100, gamma='auto', degree=3, epsilon=.1,coef0=1)
    # #reg = svm.SVR()
    # reg.fit(samples,output)
    # print(reg.predict([[160,.25,0,0]]))
    # print(reg.score(samples, output))

    # Examine model fit