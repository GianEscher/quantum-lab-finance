# Description

This **Python** algorithms utilizes a heuristic technique called **Simulated Annealing** for solving a combinatorial problem. The problem in case refers to **finding the best weight distribution for n assets in a financial portfolio**, in order to **minimize the risk** and find the correspondent return.

The method used for calculating risk and return from a certain distribution of assets **follows** the Mean Variance Model, also known as **Markowitz Model**. Moreover, there are two restrictions for the possible weights to be assigned for each asset. Being x_i the weight generated for one of n assets, we have:

- $0 <= x_i <= 1$
- $\sum_{}^{n}x_i = 1$
## User inputs

The initial parameters for users include:
* An **array** of **stock codes** (these must be available at https://finance.yahoo.com/)
* The **initial date** for the time series
* The **end date** for the time series
* The **risk acceptance parameter** $\lambda$ (Ranging from 0 - risk and return equally important, to 1 - only consider risk while minimizing).

## Outputs

The algorithm returns the **minimized value** for the **specified risk** and return combination, the return and the **asset weight distribution** for the portfolio in question.
Additionally, the **efficient frontier** diagram and the **convergence graph** for the simulated annealing process are generated into the local path.

## Algorithm versions
Three versions of this method were developed in total, differing in the approach taken to distribute the weights for each asset. Specifically, it's possible to find an adequate solution (optimal, but by heuristic standards) through continuous and discrete distribution.

The continuous version just uses a standard real positive distribution to allocate asset weights. 

Meanwhile, the discrete version receives an extra parameter $k$ that defines how many assets should be picked among the user selection. Naturally, this assets are further converted into equally real and positive values, described by $\frac{1}{k}$, before calculating the Markowitz model. 

Lastly, a custom combination of discrete selection and real modelling of each asset was implemented as a third version of the SA algorithm. For more details on this approach, please check our article **Improving the Simulated Annealing Algorithm through a combination of discrete and continuous models.**

# Detailed task flow
 
 The algorithm execution is comprised of 5 main functions:
* Retrieval of historical series from Yahoo Finance, calculus of basic values for the next steps (Standard deviation, means, variance, Pearson correlation), and risk matrix build up;
	 * The percentual errors of each historical series point are taken in account, instead of raw values;
* Calculus of risk and return based on an asset distribution parameter, following the Markowitz model;
* Execution of the first Simulated Annealing cycle, separated from the remaining cycles in order to allocate a greater amount of computational effort;
*  Execution of the remaining SA cycles, following the evolution of temperature and the 'pickyness' of Metropolis criterion;
	* If everything goes well, the result should converge at the smallest generated value for risk (i.e., the offset should be zero);
* The genral inteface, or simply main function, to manage the kickstart and the result compilation and display from the overall execution;

Moreover, you may find a merge sort function to help picking the lowest risk from each portfolio batch generated.

## Retrieving values

After receiving the initial parameters, for each specified asset, an .CSV of historical data is retreived from Yahoo Finance database. This includes daily values of opening, closing, max, min and mean prices. Each .CSV is then converted into a Pandas dataframe and stripped only for the closing prices column.

Based on the relative error for each raw value in the closing series, the mean, standard deviation, variance and Pearson covariance are calculated and stored as global constants (Not really constants since it's Python).

- Relative error approach utilized:
$$
r_{e} = \frac{x_{i+1} - x_{i}}{x_{i}}
$$

## First Simulated Annealing cycle
The SA operates in cycles, monitoring the evolution of a simulated temperature and adjusting the Metropolis criterion (the selection criteria utilized for picking the 'most promising' value). In each cycle, there will be $n_{iter}$ generated portfolios, each utilizing a continuous random asset distribution.

One of these portfolios will be selected on each cycle, just to be used as a starting point (a seed) for the next cycle generation. The random asset dsitribution will be explained soon.

Even if the risk is being minmized in this case, not necessarily the lowest value among the $n$ random portfolios of a cycle is to be selected. Sometimes, the algorithm decides for sticking with a relatively low value, in  order to avoid getting stuck in any local minima.

### Where the Markowitz model comes in
Every portfolio generated, be it at the first or at the remaining cycles, is calculated based on the Markowitz model. The asset distribution comes as a vector parameter, while means, standard deviation, variance and Pearson covariance are get from the global constants.

The function then outputs risk and return, still following the risk acceptance ($\lambda$) parameter configurated initially.

### Random asset continuous distribution
To stick with the constraints mentioned earlier, it was proposed to iterate over a vector of zeros of size $n$, while using the random uniform distribution function from Python. 

The first value generates between 1 and 0, then being subtracted from 1 and updating the range. If it happens that there is still some range remaining for the last asset, no random generation is needed, and thus this weight is defined out of the loop.

By following this for each asset weight, the two constraints can be satisfied, but the overall distribution will certainly tend to 'favor' the first values to be selected. This happens independently from the starting index for the iteration.

To contour that, a binary number (actually, 1 or -1) is sorted before the iteration, using Python binary distribution, where the positive value sets the loop to start at the index 0, while the negative sets it for the last index. This doesn't solves the problem entirely, but mitigates its effects enough over the distributions in general. 

### Random asset discrete distribution

This version of weight distribution also requires the amount $k$ of assets to be picked. Instead of 'chipping off a piece' of the range for each asset, it sorts if a position in some array of zeros will be flipped to 1, using Python binary distribution.

But by doing so, not only we have the same problem with starting indexes from the previous version, but also we may find that a number of zeros *<k* was flipped during one full iteration over the array.

Therefore, the same 'starting index sorting' from the previous version is implemented here, and the loop is made a bit more complex by being 'reversable', in case of not fulfilling its quota of *k* flips.

### Combinated distribution

Although the combined case of SA might impose a more cumbersome approach, there is no great difference in the code. Just having the two functions described above can yield the result needed.

The first array to be generated is the discrete one, which will be fed as a mask in sequence to the continuous generation. The only alteration here is a check to execute the process only for 1s in the array.

### First cycle peculiarity
As can be seen in the random asset distribution generation, no kind of seed is taken as parameter in the process. That's exactly what makes the first cycle of the SA different, since it's 'purely random', just like an exploratory analysis of the Markowitz function image for the given parameters.

This exploratory stage should usually be longer than other cycles, since the kickstart seed for the following processes will be selected from it. The SA is a heuristic approach, and thus, depending on how off are its paremeters for the simulation, relies on some level of 'luck' to work properly. Asserting a good kickstart seed right on the beggining can improve the following execution, therefore increasing result precision

*To check the theoretical and empirical basis on what was said, please check our article **Improving the Simulated Annealing Algorithm through a combination of discrete and continuous models.***

### Values for the diagrams
Lastly, it is valid to note that, for the $n_{iter}$ portfolios generated, the risk and return will be added in generation order to a global dictionary. This data will be further used for plotting the efficient frontier and the convergence graph at the end of the execution.

## Simulated annealing cycles
Thorough the execution of SA first cycle, the lowest risk is selected, as well as the corresponding asset distribution. A set of parameters pertaining to the SA configuration are defined before the reamining cycles too. Take these as a given for now, although everything is **completely explained** in **our article**. 

At each one of the $m$ cycles, $m_{iter}$ portfolios will be generated. Instead of coming up with a whole new generation for the assets, the best distribution from the last cycle will be used as basis. 

The whole purpose of this slight 'mutation' is to explore possible combinations near of the selected spot, or simply 'neighbouring solutions', which is better explained in our **article.**

- In the continuous case, the values in matter will be mutated by a factor of $\pm25$%, and then normalized for its sum to be equal to 1 again.
- For discrete values, we stablished that only a random 0 and a random 1 are flipped, which is achieved by loops sorting positions that satisfies the search and flipping it. (This is not a true neightbouring result tho, please check the material).
- The combined version picks a random non zero value from the vector, changes it to zero, and picks a random zero position to put the selected value back. After that, the same process for the continuous case is applied, mutating and normalizing only the non-zero positions.

### Selection with Metropolis criteria
The following section of the SA function implements a selection based on the metropolis criterion, as well the adjustment of simulated temperature at the end of each cycle. It is advisable to first grasp the SA concept in order to fully undestand this part of the process, although this is not needed to utilize the algorithm pratically.

## Result output
At the end of the execution, the script will output the selected risk and the corresponding return and asset distribution. If everything goes well, this should be close to the optimal solution.

The convergence and efficient frontier diagams will also be generated and stored in the local directory.

