def metric_lmnn(X, Y):
    from metric_learn import LMNN
    lmnn = LMNN(k=2, learn_rate=1e-6)
    lmnn.fit(X, Y)
    X_lmnn = lmnn.transform()
    return X_lmnn


def metric_nca(X, Y):
    from metric_learn import NCA
    nca = NCA(max_iter=1000, learning_rate=0.01)
    nca.fit(X, Y)
    X_nca = nca.transform()
    return X_nca


def metric_lfda(X, Y):
    from metric_learn import LFDA
    lfda = LFDA(k=2, num_dims=4)
    lfda.fit(X, Y)
    X_lfda = lfda.transform()
    return X_lfda


def metric_mlkr(X, Y):
    from metric_learn import MLKR
    mlkr = MLKR()
    mlkr.fit(X, Y)
    X_mlkr = mlkr.transform()
    return X_mlkr


def metric_itml_sup(X, Y):
    from metric_learn import ITML_Supervised
    itml = ITML_Supervised(num_constraints=200)
    itml.fit(X, Y)
    X_itml = itml.transform()
    return X_itml


def metric_lsml_sup(X, Y):
    from metric_learn import LSML_Supervised
    lsml = LSML_Supervised(num_constraints=200)
    lsml.fit(X, Y)
    X_lsml = lsml.transform()
    return X_lsml


def metric_sdml_sup(X, Y):
    from metric_learn import SDML_Supervised
    sdml = SDML_Supervised(num_constraints=200)
    sdml.fit(X, Y)
    X_sdml = sdml.transform()
    return X_sdml


def metric_rca_sup(X, Y):
    from metric_learn import RCA_Supervised
    rca = RCA_Supervised(num_chunks=30, chunk_size=2)
    rca.fit(X, Y)
    X_rca = rca.transform()
    return X_rca


def metric_mmc_sup(X, Y):
    from metric_learn import MMC_Supervised
    mmc = MMC_Supervised(num_constraints=200)
    mmc.fit(X, Y)
    X_mmc = mmc.transform()
    return X_mmc
