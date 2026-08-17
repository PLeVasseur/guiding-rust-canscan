//! Skeleton B, completed by an agent. The interesting part is what the
//! bodies cannot do: see the commented-out lines in the tests.

pub struct Meters(pub f64);

pub struct SessionId(u64);

impl SessionId {
    pub fn new(raw: u64) -> Self {
        SessionId(raw)
    }
}

pub struct Running {
    id: SessionId,
    samples: Vec<Meters>,
}

pub struct Finished {
    id: SessionId,
    total: Meters,
}

impl Running {
    pub fn new(id: SessionId) -> Self {
        Running {
            id,
            samples: Vec::new(),
        }
    }

    pub fn add_sample(&mut self, d: Meters) {
        self.samples.push(d);
    }

    pub fn finish(self) -> Finished {
        let total = Meters(self.samples.iter().map(|m| m.0).sum());
        Finished { id: self.id, total }
    }
}

impl Finished {
    pub fn total_km(&self) -> f64 {
        self.total.0 / 1000.0
    }

    pub fn id(&self) -> &SessionId {
        &self.id
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn normal_flow() {
        let mut session = Running::new(SessionId::new(7));
        session.add_sample(Meters(1500.0));
        session.add_sample(Meters(500.0));
        let finished = session.finish();
        assert_eq!(finished.total_km(), 2.0); // meters in, km out
    }

    #[test]
    fn the_defects_from_module_a_do_not_compile_here() {
        let mut session = Running::new(SessionId::new(8));
        session.add_sample(Meters(100.0));
        let finished = session.finish();

        // session.add_sample(Meters(1.0));
        //   error[E0382]: borrow of moved value: `session`
        //   (adding after finish: the session was consumed)

        // finished.add_sample(Meters(1.0));
        //   error[E0599]: no method named `add_sample` found for `Finished`

        // let n: f64 = finished.total_km() + Meters(3.0);
        //   error[E0277]: cannot add `Meters` to `f64`
        //   (units cannot mix unnoticed)

        // There is no `state` string to typo and no `done` flag to
        // disagree with it. Those fields do not exist.
        assert_eq!(finished.total_km(), 0.1);
    }
}
