import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal as mvn
from scipy.stats import norm
from numpy.random import normal
from scipy.stats import t

from IPython.display import display
from ipywidgets import FloatSlider, IntSlider, Button

class cor_coef_demo:
    def __init__(self):
        def update_slider(_):
            # set r to the slider value and replot
            self.r = r_sl.value
            plot()

        def plot():
            # clear plot
            ax.cla()
            if self.r >= 0:
                # if r is positive move points towards y=x
                xp = a + (1-self.r) * b
                yp = a - (1-self.r) * b
            elif self.r < 0:
                # if r is negative move points towards y=-x
                xp = (1+self.r) * a + b
                yp = (1+self.r) * a - b

            # scatter plot of points removing tick labels and set title to r
            ax.scatter(xp, yp, edgecolors='k', alpha=0.5)
            ax.set_xlim(-4, 4)
            ax.set_ylim(-4, 4)
            ax.set_xlabel('Variable 1')
            ax.set_ylabel('Variable 2')
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_title(f'$r$ = {self.r:.2f}', size=20)

        # 100 random variates from a bivariate normal distribution with mean 0, and identity covariance matrix
        xs = mvn.rvs([0, 0], size=100)
        # save variates into x and y and set up a and b for transformation in plot()
        x, y = xs[:,0], xs[:,1]
        a = 0.5*(x + y)
        b = 0.5*(x - y)
        # set initial cor. coef. to 0
        self.r = 0

        # set up a slider for r from -1 to 1
        r_sl = FloatSlider(min=-1, max=1, value=self.r, step=0.01,  layout={'width':'200pt'},
                           style={'description_width':'initial', 'handle_color':'Blue'},)
        r_sl.observe(update_slider, 'value')
        display(r_sl)

        # initialise figure removing unnecessary clutter
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.canvas.footer_visible = False
        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = False
        plot()
        plt.ion()


class slider_props:
    def __init__(self, minv, maxv, step, init):
        """set a slider's properties"""
        self.minv = minv
        self.maxv = maxv
        self.step = step
        self.init = init

class pop_est:
    def __init__(self):
        def update_slider(_):
            self.mu = mu_sl.value
            self.sigma = sigma_sl.value
            self.n = n_sl.value
            plot()

        def plot():
            # Population distribution
            ax = axs[0]
            ax.cla()

            xt = np.linspace(0, 100, 100)
            yt = norm.pdf(xt, self.mu, self.sigma)
            ax.fill_between(xt, 0, yt, alpha=0.5)

            yc = ax.get_ylim()
            ax.text(0, 0.5*(yc[0]+yc[1]),
                    r'$\mu$ = ' f'{self.mu:.2f}\n'
                    r'$\sigma$ = ' f'{self.sigma:.2f}',
                    ha='left', ma='left', color='C1', fontsize=10)

            ax.set_xlabel('Dive duration (mins)')
            ax.set_yticks([])
            ax.set_yticklabels([])
            ax.set_ylim(0, ax.get_ylim()[1])
            ax.set_title('Population distribution')

            # Data distribution
            ax = axs[1]
            ax.cla()
            bins = np.linspace(0, 100, 50)

            sample = normal(self.mu, self.sigma, size=self.n)
            xbar = sample.mean()
            std = sample.std()
            sem = std/np.sqrt(self.n)
            # tn = t.ppf(0.975, df=self.n-1)

            ax.hist(sample, bins=bins, alpha=0.5, color='C0', ec='k')

            # ax.errorbar(xbar, 25, xerr=s['sem'], capsize=3, color='C0')
            ax.text(self.mu, 25,
                    r'$\hat{\mu}$ = '
                    f'{xbar:.2f} ± {sem:.2f} mins',
                    # f'\n95% CI: [{xbar - tn*sem:.2f}, {xbar + tn*sem:.2f}]',
                    ha='center', ma='center', color='C0', fontsize=12)

            ax.text(0, 15,
                    r'$\bar{x}$ = ' f'{xbar:.2f}\n'
                    r'$s$ = ' f'{std:.2f}',
                    ha='left', ma='left', color='C1', fontsize=10)

            ax.set_xlabel('Dive duration (mins)')
            ax.set_ylabel('Number of dives')
            ax.set_ylim(0, 30)
            ax.set_title('Data distribution')

            # Sampling distribution
            ax = axs[2]
            ax.cla()

            xt = np.linspace(self.mu-5*sem, self.mu+5*sem, 100)
            yt = norm.pdf(xt, self.mu, sem)
            ax.fill_between(xt, 0, yt, alpha=0.5)

            yc = ax.get_ylim()
            ax.text(0, 0.5*(yc[0]+yc[1]),
                    rf'SEM = $\frac{{{std:.2f}}}{{\sqrt{{{self.n}}}}}$'
                    f' = {sem:.2f} mins',
                    ha='left', ma='center', color='C1', fontsize=12)

            ax.set_xlabel('Mean dive duration (mins)')
            ax.set_xlim(axs[1].get_xlim())
            ax.set_yticks([])
            ax.set_yticklabels([])
            ax.set_ylim(0, ax.get_ylim()[1])
            ax.set_title('Sampling distribution of the mean')

        self.mu = 50
        self.sigma = 10
        self.n = 200
        self.sem = self.sigma / np.sqrt(self.n)

        mu_sl = FloatSlider(min=25, max=75, value=self.mu, step=1, layout={'width':'50%'}, style={'description_width':'initial', 'handle_color':'LightBlue'}, description='Population mean dive duration')
        sigma_sl = FloatSlider(min=1, max=20, value=self.sigma, step=1, layout={'width':'50%'}, style={'description_width':'initial', 'handle_color':'LightBlue'}, description='Population st. dev. of dive duration')
        n_sl = IntSlider(min=5, max=self.n, value=self.n, step=1, layout={'width':'50%'}, style={'description_width':'initial', 'handle_color':'LightBlue'}, description='Sample size')

        for s in [mu_sl, sigma_sl, n_sl]:
            s.observe(update_slider, 'value')
            display(s)

        fig, axs = plt.subplots(3, 1, figsize=(6, 9))
        fig.subplots_adjust(hspace=0.5)
        for ax in axs.flatten():
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        fig.canvas.footer_visible = False
        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = False
        plot()
        plt.ion()
