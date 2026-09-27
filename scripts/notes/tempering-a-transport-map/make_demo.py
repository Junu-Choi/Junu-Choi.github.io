"""Build a reproducible, CPU-only illustration of transport-map compatibility.

Run with Python + numpy, scipy, matplotlib. No trained model or manuscript files
are used. This is one exact rematching step at a known mixture posterior, not a
benchmark of the finite PTM sampler. The slider changes the map, not the target.
"""
from pathlib import Path
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr, logsumexp


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "public/notes/tempering-a-transport-map"
TAU, OBSERVATION, OBS_VARIANCE = 0.8, 0.25, 0.3**2
SEED, SAMPLE_COUNT = 260927, 160
GAMMAS = np.linspace(0.25, 1, 31)
PLOT_LIMIT, INPUT_LIMIT = 3.0, 4.5
LEFT, RIGHT, TOP, BOTTOM = 32, 264, 12, 244


class Mixture:
    def __init__(self, weights, means, variances):
        self.w = np.asarray(weights, dtype=float)
        self.m = np.asarray(means, dtype=float)
        self.v = np.asarray(variances, dtype=float)

    def pdf(self, x):
        z = np.asarray(x)[..., None] - self.m
        return np.sum(self.w * np.exp(-z*z/(2*self.v)) / np.sqrt(2*np.pi*self.v), axis=-1)

    def cdf(self, x):
        return np.sum(self.w * ndtr((np.asarray(x)[..., None]-self.m)/np.sqrt(self.v)), axis=-1)

    def ppf(self, u):
        u = np.clip(np.asarray(u), 1e-15, 1-1e-15)
        lo = np.full_like(u, float(np.min(self.m-12*np.sqrt(self.v))))
        hi = np.full_like(u, float(np.max(self.m+12*np.sqrt(self.v))))
        for _ in range(57):
            mid = (lo+hi)/2
            below = self.cdf(mid) < u
            lo = np.where(below, mid, lo)
            hi = np.where(below, hi, mid)
        return (lo+hi)/2

    def heat(self):
        return Mixture(self.w, self.m, self.v+TAU)


PRIOR = Mixture([0.4, 0.6], [-1.3, 1.3], [0.35**2, 0.45**2])


def tempered(gamma):
    v = 1/(1/PRIOR.v + gamma/OBS_VARIANCE)
    m = v*(PRIOR.m/PRIOR.v + gamma*OBSERVATION/OBS_VARIANCE)
    log_w = np.log(PRIOR.w) + 0.5*np.log(v/PRIOR.v) - 0.5*(
        PRIOR.m**2/PRIOR.v + gamma*OBSERVATION**2/OBS_VARIANCE - m*m/v)
    return Mixture(np.exp(log_w-logsumexp(log_w)), m, v)


TARGET, PRIOR_HEAT = tempered(1), PRIOR.heat()
GAUSSIAN_INPUT = TARGET.heat()


def transport(x, distribution):
    return distribution.ppf(distribution.heat().cdf(x))


def inverse_transport(z, distribution):
    return distribution.heat().ppf(distribution.cdf(z))


def derivative(x, distribution):
    return distribution.heat().pdf(x)/distribution.pdf(transport(x, distribution))


def required_input_pdf(x, distribution):
    z = transport(x, distribution)
    return TARGET.pdf(z) * distribution.heat().pdf(x)/distribution.pdf(z)


def xy(points, xlim=PLOT_LIMIT, ylim=PLOT_LIMIT):
    points = np.asarray(points)
    x = LEFT+(points[:, 0]+xlim)*(RIGHT-LEFT)/(2*xlim)
    y = BOTTOM-(points[:, 1]+ylim)*(BOTTOM-TOP)/(2*ylim)
    return np.column_stack([x, y])


def path(points, close=False):
    pairs = [f"{x:.2f},{y:.2f}" for x, y in np.asarray(points)]
    return "M"+"L".join(pairs)+("Z" if close else "")


def dot_path(points):
    # A circle path keeps the interactive SVG DOM small.
    return "".join(f"M{x-1.7:.2f},{y:.2f}a1.7,1.7 0 1,0 3.4,0a1.7,1.7 0 1,0 -3.4,0Z" for x, y in xy(points))


def map_points(points, distribution):
    return np.column_stack([transport(points[:, 0], distribution), transport(points[:, 1], PRIOR)])


def density_path(x, values, ymax):
    px = LEFT+(x+INPUT_LIMIT)*(RIGHT-LEFT)/(2*INPUT_LIMIT)
    py = BOTTOM-values*(BOTTOM-TOP)/ymax
    return path(np.column_stack([px, py]))


def main():
    rng = np.random.default_rng(SEED)
    uniforms = rng.uniform(0, 1, (SAMPLE_COUNT, 2))
    target_samples = np.column_stack([TARGET.ppf(uniforms[:, 0]), PRIOR.ppf(uniforms[:, 1])])
    reference_samples = np.column_stack([GAUSSIAN_INPUT.ppf(uniforms[:, 0]), PRIOR_HEAT.ppf(uniforms[:, 1])])
    xcurve = np.linspace(-INPUT_LIMIT, INPUT_LIMIT, 401)
    distributions = [tempered(gamma) for gamma in GAMMAS]
    required_curves = [required_input_pdf(xcurve, d) for d in distributions]
    ymax = np.ceil(max(max(p) for p in required_curves)*10)/10
    ymax = max(ymax, np.ceil(max(GAUSSIAN_INPUT.pdf(xcurve))*10)/10)

    edges = np.linspace(-2, 2, 9)
    grid_lines = []
    for edge in edges:
        grid_lines += [np.array([[edge, -2], [edge, 2]]), np.array([[-2, edge], [2, edge]])]
    # The map is coordinatewise, so input rectangles map to exact rectangles.
    cell = np.array([[0.5, 0.5], [1, 0.5], [1, 1], [0.5, 1]])
    source_grid = "".join(path(xy(line)) for line in grid_lines)

    # Fixed 50% and 90% highest-density contours of the actual target mixture.
    grid = np.linspace(-PLOT_LIMIT, PLOT_LIMIT, 601)
    xx, yy = np.meshgrid(grid, grid)
    density = TARGET.pdf(xx)*PRIOR.pdf(yy)
    dx = grid[1]-grid[0]
    ordered = np.sort(density.ravel())[::-1]
    mass = np.cumsum(ordered)*dx*dx
    levels = [float(ordered[np.searchsorted(mass, p)]) for p in [0.9, 0.5]]
    fig, ax = plt.subplots()
    contour = ax.contour(xx, yy, density, levels=levels)
    contours = ["".join(path(xy(poly), close=True) for poly in p.to_polygons()) for p in contour.get_paths()]
    plt.close(fig)

    frames = []
    worst = {"matched_sample_error": 0.0, "required_input_mass_error": 0.0,
             "jacobian_relative_error": 0.0, "cell_area_relative_error": 0.0,
             "tv_coordinate_invariance_error": 0.0, "cdf_round_trip_error": 0.0}
    probabilities = np.linspace(1e-5, 1-1e-5, 201)
    # Fixed probability bins give an independent check of output total variation.
    edges_z = TARGET.ppf(np.linspace(1e-9, 1-1e-9, 16001))
    reference_bins = np.diff(TARGET.cdf(edges_z))
    for gamma, distribution, curve in zip(GAMMAS, distributions, required_curves):
        mapped_grid = "".join(path(xy(map_points(line, distribution))) for line in grid_lines)
        mapped_cell = map_points(cell, distribution)
        area = float((mapped_cell[1, 0]-mapped_cell[0, 0])*(mapped_cell[2, 1]-mapped_cell[1, 1])/0.25)
        gaussian_samples = map_points(reference_samples, distribution)
        matched_x = inverse_transport(target_samples[:, 0], distribution)
        matched_y = inverse_transport(target_samples[:, 1], PRIOR)
        recovered = map_points(np.column_stack([matched_x, matched_y]), distribution)
        worst["matched_sample_error"] = max(worst["matched_sample_error"], float(np.max(np.abs(recovered-target_samples))))
        assert np.max(np.abs(gaussian_samples)) < PLOT_LIMIT
        assert np.max(np.abs(target_samples)) < PLOT_LIMIT
        assert np.max(np.abs(mapped_cell)) < PLOT_LIMIT

        # Independent quadrature checks the displayed area and input density.
        required_mass = quad(lambda x: float(required_input_pdf(x, distribution)), -10, 10, epsabs=2e-9, limit=150)[0]
        required_mean = quad(lambda x: float(x*required_input_pdf(x, distribution)), -10, 10, epsabs=2e-9, limit=150)[0]
        tv = quad(lambda x: float(abs(required_input_pdf(x, distribution)-GAUSSIAN_INPUT.pdf(x)))/2,
                  -10, 10, epsabs=2e-8, limit=150)[0]
        output_cdf = GAUSSIAN_INPUT.cdf(inverse_transport(edges_z, distribution))
        tv_output = (np.sum(np.abs(np.diff(output_cdf)-reference_bins))
                     + abs(output_cdf[0]-1e-9) + abs(1-output_cdf[-1]-1e-9))/2
        worst["required_input_mass_error"] = max(worst["required_input_mass_error"], abs(required_mass-1))
        worst["tv_coordinate_invariance_error"] = max(worst["tv_coordinate_invariance_error"], float(abs(tv-tv_output)))
        expected_area = quad(lambda x: float(derivative(x, distribution)), 0.5, 1)[0] * quad(lambda x: float(derivative(x, PRIOR)), 0.5, 1)[0]/0.25
        worst["cell_area_relative_error"] = max(worst["cell_area_relative_error"], abs(expected_area-area)/area)
        check_x = np.linspace(-2.5, 2.5, 101)
        finite_difference = (transport(check_x+1e-5, distribution)-transport(check_x-1e-5, distribution))/2e-5
        worst["jacobian_relative_error"] = max(worst["jacobian_relative_error"], float(np.max(np.abs(finite_difference/derivative(check_x, distribution)-1))))
        for d in [distribution, distribution.heat()]:
            worst["cdf_round_trip_error"] = max(worst["cdf_round_trip_error"], float(np.max(np.abs(d.cdf(d.ppf(probabilities))-probabilities))))

        frames.append({"gamma": round(float(gamma), 3), "volumeGrid": mapped_grid,
                       "volumeCell": path(xy(mapped_cell), close=True), "inputRequired": density_path(xcurve, curve, ymax),
                       "samplesGaussian": dot_path(gaussian_samples), "areaRatio": round(area, 6), "tv": round(float(tv), 7),
                       "inputMeanShift": round(float(required_mean-np.sum(GAUSSIAN_INPUT.w*GAUSSIAN_INPUT.m)), 6)})

    # Fully conditioned map + posterior heat input must preserve the posterior.
    assert worst["matched_sample_error"] < 1e-9, worst
    assert worst["required_input_mass_error"] < 1e-7, worst
    assert worst["jacobian_relative_error"] < 1e-6, worst
    assert worst["cell_area_relative_error"] < 1e-8, worst
    assert worst["tv_coordinate_invariance_error"] < 2e-5, worst
    assert worst["cdf_round_trip_error"] < 1e-12, worst
    assert frames[-1]["tv"] < 1e-8
    assert frames[-1]["samplesGaussian"] == dot_path(target_samples)
    assert frames[-1]["inputRequired"] == density_path(xcurve, GAUSSIAN_INPUT.pdf(xcurve), ymax)

    payload = {"defaultIndex": 0, "frames": frames,
               "static": {"volumeSource": source_grid, "cellSource": path(xy(cell), close=True),
                          "inputGaussian": density_path(xcurve, GAUSSIAN_INPUT.pdf(xcurve), ymax),
                          "samplesMatched": dot_path(target_samples), "targetContours": contours,
                          "inputDensityMax": float(ymax)},
               "model": {"prior": {"weights": PRIOR.w.tolist(), "means": PRIOR.m.tolist(), "std": np.sqrt(PRIOR.v).tolist()},
                         "observation": OBSERVATION, "observationVariance": OBS_VARIANCE, "noiseVariance": TAU,
                         "seed": SEED, "samples": SAMPLE_COUNT, "targetGamma": 1,
                         "description": "Independent two-coordinate mixture prior. Observe coordinate 1. One exact map/rematching step with a known target; no finite PTM sampler or trained model.",
                         "pairing": "Fixed uniform random numbers shared by both input laws at every gamma; matching uses the analytic target. All generated samples are shown. Metrics integrate the full laws.",
                         "tv": "Total variation between Gaussian-input output and target; equal to TV between Gaussian and required inputs under the invertible map.",
                         "contours": "Fixed target highest-density regions at probability masses 0.5 and 0.9."}}
    verification = {"generatorSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    "checks": worst, "frames": len(frames), "targetMassWithinPlot": float(mass[-1]),
                    "endpointTV": frames[-1]["tv"], "defaultTV": frames[0]["tv"],
                    "scope": payload["model"]["description"]}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"demo.json").write_text(json.dumps(payload, separators=(",", ":"))+"\n")
    (OUT/"verification.json").write_text(json.dumps(verification, indent=2)+"\n")
    print(json.dumps(verification, indent=2))
    print(f"demo.json: {(OUT/'demo.json').stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
